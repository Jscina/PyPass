import logging
from abc import ABC, abstractmethod

from authentication import Auth
from flask import Response, jsonify, request
from models import Account, Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class AbstractDatabase(ABC):
    
    @abstractmethod
    def create_user(self, username: str, password: str) -> str | None:
        pass

    @abstractmethod
    def create_account(self, website: str, username: str, password: str) -> bool:
        pass

    @abstractmethod
    def fetch_login(self, email: str | None, username: str | None) -> list[tuple]:
        pass

    @abstractmethod
    def login(self, email: str | None, username: str | None, password: str) -> bool:
        pass

    @abstractmethod
    def close(self):
        pass


class Database(AbstractDatabase):
    """PyPass Database interface"""
    db_name: str = "pypass.sqlite"

    def __init__(self) -> None:
        engine = create_engine(f'sqlite:///{self.db_name}')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.auth = Auth()

    def create_user(self, email: str, username: str, password: str) -> str | None:
        hashed_password = self.auth.hash_password(password)
        user = User(email=email, username=username, password=hashed_password)
        self.session.add(user)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            return f"Error creating user: {e}"

    def create_account(self, website: str, username: str, password: str) -> bool | str:
        key = self.auth.generate_key()
        protected_password = self.auth.encrypt_str(password, key)
        protected_key = self.auth.encrypt_key(key)
        user = self.session.query(User).filter(
            User.username == username).first()
        account = Account(
            user_id=user.id,
            website=website,
            account_name=username,
            account_username=username,
            account_password=protected_password,
            encryption_key=protected_key
        )
        self.session.add(account)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            return f"Error creating account: {e}"
        return True

    def fetch_login(self, email: str | None, username: str | None) -> list[tuple[str, str]]:
        """Collects the possible accounts that match the username or email"""
        if username is not None:
            user = self.session.query(User).filter(
                User.username == username).first()
        elif email is not None:
            email = self.session.query(User).filter(
                User.email == email).first()
        else:
            return []
        users = self.session.query(User).filter(User.username == user).all()
        return [(user.username, user.password) for user in users]

    def login(self, email: str | None, username: str | None, password: str) -> bool:
        users = self.fetch_login(email, username)
        for account_username, account_password in users:
            verify_password = self.auth.verify_password(
                password, account_password)
            verify_user = self.auth.compare(
                username, account_username) or self.auth.compare(email, account_username)
            if verify_user and verify_password:
                return True
        return False

    def close(self):
        self.session.close()


def get_database() -> Database | Response:
    db: Database = getattr(request, "db", None)
    if db is None:
        logger.error("No database found in request context")
        return jsonify({"status": "error", "message": "Internal server error"}), 500
    return db
