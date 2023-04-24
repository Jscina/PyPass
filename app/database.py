import logging
from dataclasses import dataclass
from typing import Optional
from authorization import verify_username, verify_password
from cipher import Cipher
from flask import Response, jsonify, request
from models import Account, Base, Master_Key, User
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker, Session


@dataclass
class Database:
    """The Database class handles all database operations"""
    cipher: Cipher
    db_name: str = "pypass.sqlite"

    def __post_init__(self) -> None:
        engine = create_engine(f'sqlite:///{self.db_name}')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self._session = Session()

    @property
    def session(self) -> Session:
        return self._session

    def fetch_master_key(self, user: User) -> bytes:
        """Get the master key from the database."""
        try:
            key = self.session.query(Master_Key) \
                .filter(Master_Key.user_id == user.id).one()
            return key
        except NoResultFound:
            logging.warning("No result's from query, creating new key...")
            self.cipher.master_key = self.add_master_key(user=user)
            return self.fetch_master_key()

    def add_master_key(self, user: User) -> bytes:
        """Add a new master key for the user to the database"""
        key = self.cipher.generate_key()
        master_key = Master_Key(master_key=key.decode('utf-8'))
        master_key.user_id = user.id
        try:
            self.session.add(master_key)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error creating master key: {e}")
        return key

    def add_user(self, email: str, username: str, password: str) -> str | None:
        """Create a new login account"""
        hashed_password = self.cipher.hash_password(password)
        key = self.cipher.generate_key()
        master_key = Master_Key(master_key=key.decode('utf-8'))
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

    def add_account(self, website: str, username: str, password: str) -> bool | str:
        """Add a new account for storing user's credentials to other sites/applications"""
        key = self.cipher.generate_key()
        protected_password, protected_key = self.cipher.encrypt(
            password, key, encrypt_key=True)
        user_id = request.cookies.get('user_id')

        if user_id is not None:
            user_id = int(user_id)

        account = Account(
            website=website,
            account_name=username,
            account_username=username,
            account_password=protected_password,
            encryption_key=protected_key
        )
        account.user_id = user_id
        try:
            self.session.add(account)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            return f"Error creating account: {e}"
        return True

    def fetch_user(self, email: Optional[str], username: Optional[str]) -> list[User]:
        """Collects the possible accounts that match the username or email"""
        if username is not None and email is not None:
            raise ValueError("Email or username must be provided")
        if username is not None:
            users = self.session.query(User) \
                .filter(User.username == username).all()
        elif email is not None:
            users = self.session.query(User) \
                .filter(User.email == email).all()
        else:
            return []
        return [user for user in users]

    def fetch_accounts(self, is_authorized: bool, user_id: str) -> list[Account]:
        """Fetches all accounts from the database"""
        if is_authorized:
            accounts = self.session.query(Account) \
                .filter(Account.user_id == user_id).all()
            for account in accounts:
                account.account_password = self.cipher.decrypt(
                    account.account_password,
                    account.encryption_key,
                    encrypt_key=True
                )
            return accounts
        return []

    def login(self, password: str, email: Optional[str] = None, username: Optional[str] = None) -> tuple[bool, User] | bool:
        """Logs the user into the application"""
        if email is None and username is None:
            raise ValueError("Email or username must be provided")

        users = self.fetch_user(email, username)
        for user in users:
            password_verified = verify_password(
                password, user.password
            )
            verify_account = email or username
            account_verified = verify_username(
                verify_account,
                user.username
            )
            if account_verified and password_verified:
                return (True, user)
        return False

    def close(self):
        self.session.close()


def get_database() -> Database | Response:
    """Get the database object from the request"""
    db: Database = getattr(request, "db", None)
    if db is None:
        return jsonify({"status": "error", "message": "Internal server error"}), 500
    return db
