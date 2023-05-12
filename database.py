import logging
from dataclasses import dataclass
from typing import Optional
from authorization import verify_username, verify_password
from fastapi.exceptions import HTTPException
from cipher import Cipher, Cipher_User
from models import Account, Base, Master_Key, User
from sqlalchemy import create_engine, func, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker, Session


@dataclass(unsafe_hash=True)
class Database:
    """The Database class handles all database operations"""

    cipher: Cipher
    db_name: str = "pypass.sqlite"

    def __post_init__(self) -> None:
        engine = create_engine(f"sqlite:///{self.db_name}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self._session = Session()

    @property
    def session(self) -> Session:
        return self._session

    async def fetch_master_key(self, user: User) -> bytes:
        """Get the master key from the database."""
        try:
            key:str = (
                self.session.query(Master_Key)
                .filter(Master_Key.user_id == user.id)
                .one()
            ).master_key
            return key.encode("utf-8")
        except NoResultFound:
            logging.warning("No result's from query, creating new key...")
        self.cipher.master_key = await self.add_master_key(user=user)
        return self.fetch_master_key()

    async def add_master_key(self, user: User) -> bytes:
        """Add a new master key for the user to the database"""
        key = await self.cipher.generate_key()
        master_key = Master_Key(master_key=key.decode("utf-8"))
        master_key.user_id = user.id
        try:
            self.session.add(master_key)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error creating master key: {e}")
        return key

    async def add_user(self, email: str, username: str, password: str) -> str | None:
        """Create a new login account"""
        hashed_password = await self.cipher.hash_password(password)
        key = await self.cipher.generate_key()
        master_key = Master_Key(master_key=key.decode("utf-8"))
        user = User(email=email, username=username, password=hashed_password)
        user.master_key = master_key
        transactions = (user, master_key)
        try:
            for transaction in transactions:
                self.session.add(transaction)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            return f"Error creating user: {e}"

    async def add_account(
        self, account_data: dict[str, str]
    ) -> bool | str:
        """Add a new account for storing user's credentials to other sites/applications"""
        key = await self.cipher.generate_key()
        protected_password, protected_key = await self.cipher.encrypt(
            account_data["password"], key, encrypt_key=True
        )
        user_id = account_data["user_id"]

        if user_id is not None:
            user_id = int(user_id)
        else:
            return "Error: User is invalid"
        max_order = self.session.query(func.max(Account.account_order)).scalar() or 0
        account = Account(
            account_order=max_order + 1,
            service=account_data["service"],
            account_username=account_data["username"],
            account_password=protected_password,
            encryption_key=protected_key,
        )
        account.user_id = user_id
        try:
            self.session.add(account)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            return f"Error creating account: {e}"
        return True

    async def fetch_user(self, email: Optional[str], username: Optional[str]) -> list[User]:
        """Collects the possible accounts that match the username or email"""
        if username is not None and email is not None:
            raise ValueError("Email or username must be provided")
        if username is not None:
            users = self.session.query(User).filter(User.username == username).all()
        elif email is not None:
            users = self.session.query(User).filter(User.email == email).all()
        else:
            raise HTTPException(404, "No user found")
        return [user for user in users]
    
    async def fetch_user_by_id(self, is_authorized:bool, user_id:int) -> User:
        if not is_authorized:
            raise HTTPException(401, "Not Authorized")
        if isinstance(user_id, str):
            user_id = int(user_id)
        user = self.session.query(User).filter(User.id == user_id).one()
        return user


    async def fetch_accounts(self, is_authorized: bool, user_id: int) -> list[Account]:
        """Fetches all accounts from the database"""
        if not is_authorized:
            raise HTTPException(401, "Not Authorized")
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        accounts = (
            self.session.query(Account).filter(Account.user_id == user_id).all()
        )
        for account in accounts:
            account.account_password = await self.cipher.decrypt(
                protected=account.account_password,
                key=account.encryption_key,
                encrypted_key=True
            )
        if len(accounts) != 0:
            return accounts
        raise HTTPException(404, "No accounts found")
    
    async def remove_account(self, is_authorized:bool, order:int, user_id:int) -> None:
        if not is_authorized:
            raise HTTPException(401, "Not Authorized")
        
        accounts = self.session.query(Account).filter(
            Account.user_id == user_id
        ).order_by(Account.account_order).all()
        try:
            account_to_delete = accounts[order - 1]
            self.session.delete(account_to_delete)
            self.session.commit()
            await self.reindex_all_accounts()
        except NoResultFound:
            logging.warning(f"No result found for id: {order} user_id: {user_id}")
        
    async def reindex_all_accounts(self):
        accounts = self.session.query(Account).order_by(Account.user_id, Account.account_order).all()
        for i, account in enumerate(accounts, start=1):
            account.account_order = i
        self.session.commit()
        
    async def login(
        self, password: str, email: Optional[str] = None, username: Optional[str] = None
    ) -> tuple[bool, User] | bool:
        """Logs the user into the application"""
        if email is None and username is None:
            raise ValueError("Email or username must be provided")

        users = await self.fetch_user(email, username)
        for user in users:
            password_verified = verify_password(password, user.password)
            verify_account = email or username
            account_verified = verify_username(verify_account, user.username)
            if account_verified and password_verified:
                return (True, user)
        return False

    def close(self):
        self.session.close()

def get_database() -> Database:
    return Database(cipher=Cipher_User())

def close_db(database: Database) -> None:
    database.close()