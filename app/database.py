import logging
from typing import Optional

from authorization import verify_password, verify_username
from cipher import Cipher, Cipher_User
from fastapi import Request
from fastapi.responses import JSONResponse
from models import Account, Base, Master_Key, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from dataclasses import dataclass

@dataclass
class Database:
    """The Database class handles all database operations"""
    cipher: Cipher
    db_name: str = "pypass.sqlite"

    async def __post_init__(self) -> None:
        engine = create_async_engine(f'sqlite+aiosqlite:///{self.db_name}')
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        self.__session = async_scoped_session(sessionmaker(engine, class_=AsyncSession))

    @property
    def session(self) -> AsyncSession:
        return self.__session()

    async def fetch_master_key(self, user: User) -> bytes:
        """Get the master key from the database."""
        async with self.session.begin():
            try:
                key = (await self.session.execute(
                    select(Master_Key).filter(Master_Key.user_id == user.id)
                )).scalar_one()
                return key
            except NoResultFound:
                logging.warning("No result's from query, creating new key...")
                self.cipher.master_key = await self.add_master_key(user=user)
                return await self.fetch_master_key(user)

    async def add_user(self, email: str, username: str, password: str) -> str | None:
        """Create a new login account"""
        hashed_password = self.cipher.hash_password(password)
        key = self.cipher.generate_key()
        master_key = Master_Key(master_key=key.decode('utf-8'))
        user = User(email=email, username=username, password=hashed_password)
        user.master_key = master_key
        transactions = (user, master_key)
        async with self.session.begin():
            try:
                for transaction in transactions:
                    self.session.add(transaction)
            except Exception as e:
                await self.session.rollback()
                return f"Error creating user: {e}"

    async def add_account(self, website: str, username: str, password: str, request: Request) -> bool | str:
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
        async with self.session.begin():
            try:
                self.session.add(account)
            except Exception as e:
                return f"Error creating account: {e}"
        return True

    async def fetch_user(self, email: Optional[str], username: Optional[str]) -> list[User]:
        """Collects the possible accounts that match the username or email"""
        if username is None and email is None:
            raise ValueError("Email or username must be provided")
        async with self.session.begin():
            if username is not None:
                users = (await self.session.execute(
                    select(User).filter(User.username == username)
                )).scalars().all()
            elif email is not None:
                users = (await self.session.execute(
                    select(User).filter(User.email == email)
                )).scalars().all()
            else:
                return []
        return [user for user in users]

    async def fetch_accounts(self, is_authorized: bool, user_id: str) -> list[Account]:
        """Fetches all accounts from the database"""
        if is_authorized:
            async with self.session.begin():
                accounts = (await self.session.execute(
                    select(Account).filter(Account.user_id == user_id)
                )).scalars().all()
            for account in accounts:
                account.account_password = self.cipher.decrypt(
                    account.account_password,
                    account.encryption_key,
                    encrypt_key=True
                )
            return accounts
        return []

    async def login(self, password: str, email: Optional[str] = None, username: Optional[str] = None) -> tuple[bool, User] | bool:
        """Logs the user into the application"""
        if email is None and username is None:
            raise ValueError("Email or username must be provided")

        users = await self.fetch_user(email, username)
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

def get_database() -> Database | JSONResponse:
    """Get the database instance"""
    db: Database = Database(cipher=Cipher_User())
    if db is None:
        return JSONResponse(content={"status": "error", "message": "Internal server error"}, status_code=500)
    return db
