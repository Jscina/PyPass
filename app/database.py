import logging
from dataclasses import dataclass
from typing import Optional
from authorization import Auththorizer_User
from cipher import Cipher_User
from flask import Response, jsonify, request
from models import Account, Base, Master_Key, User
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker


@dataclass
class Database:
    """The Database class handles all database operations"""
    db_name: str = "pypass.sqlite"

    def __post_init__(self) -> None:
        engine = create_engine(f'sqlite:///{self.db_name}')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
    
    @property
    def cipher(self) -> Cipher_User:
        return Cipher_User(self.session)

    def fetch_master_key(self, user: User) -> bytes:
        """Get the master key from the database.
        
        Args:
            user_id (int): The user's id
        
        Returns:
            bytes: The master key
        """
        try:
            key = self.session.query(Master_Key) \
                .filter(Master_Key.user_id == user.id).one()
            return key
        except NoResultFound:
            logging.warning("No result's from query, creating new key...")
            self.cipher.master_key = self.create_master_key()
            return self.fetch_master_key()
        
    def create_master_key(self, user: User) -> bytes:
        """Add a new master key for the user to the database

        Args:
            user (User): The user object

        Returns:
            bytes: The master key
        """
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
        
        
    def create_user(self, email: str, username: str, password: str) -> str | None:
        """Create a new login account

        Args:
            email (str): User's email
            username (str): User's username
            password (str): User's password

        Returns:
            str | None: Returns a string with the error if the insertion fails for display otherwise returns None
        """
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

    def create_account(self, website: str, username: str, password: str) -> bool | str:
        """Add a new account for storing user's credentials to other sites/applications

        Args:
            website (str): The website the account is associated with
            username (str): The username
            password (str): The password

        Returns:
            bool | str: Returns True if successful otherwise returns the error message for display
        """
        key = self.auth.generate_key()
        protected_password = self.auth.encrypt_str(password, key)
        protected_key = self.auth.encrypt_key(key)
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
        """Collects the possible accounts that match the username or email

            Either username or email must be passed into this method

            Args:
                email (Optional[str]): The user's email, optional
                username (Optional[str]): The user's username, optional

            Return:
                list[User]: Returns a list of the Users
        """
        if username is not None:
            users = self.session.query(User) \
                .filter(User.username == username).all()
        elif email is not None:
            users = self.session.query(User) \
                .filter(User.email == email).all()
        else:
            return []
        return [user for user in users]

    def login(self, password: str, email: Optional[str] = None, username: Optional[str] = None) -> tuple[bool, User] | bool:
        """Logs the user into the application

        Args:
            password (str): The user's password, required
            email (Optional[str], optional): The user's email. Defaults to None.
            username (Optional[str], optional): The user's username. Defaults to None.
            
            Either username or email must be entered

        Returns:
            tuple[bool, User] | bool: Returns a tuple of a boolean and the user if successful otherwise returns False
        """
        users = self.fetch_user(email, username)
        for user in users:
            verify_password = self.auth.verify_password(
                password, user.password
                )
            if email is not None:
                verify_account = email
            elif username is not None:
                verify_account = username
            verify_account = self.auth.compare(
                verify_account,
                user.username
            )
            if verify_account and verify_password:
                return (True, user)
        return False

    def close(self):
        self.session.close()


def get_database() -> Database | Response:
    """Get the database object from the request

    Returns:
        Database | Response: Returns the database object or a response with an error message
    """
    db: Database = getattr(request, "db", None)
    if db is None:
        return jsonify({"status": "error", "message": "Internal server error"}), 500
    return db
