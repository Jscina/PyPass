import hmac
import logging
from abc import ABC, abstractmethod
from typing import Optional

import bcrypt
# from os import environ
from cryptography.fernet import Fernet
from cryptography.hazmat import backends
from models import Master_Key, User
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from flask import request

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

log = logging.getLogger(__name__)


class AuthInterface(ABC):
    """Abstract base class for the Authentication class."""
    @property
    @abstractmethod
    def master_key(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def hash_password(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_master_key(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def generate_key(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def encrypt_str(self, unprotected_str: str, key: bytes) -> str:
        raise NotImplementedError

    @abstractmethod
    def decrypt_str(self, protected_str: str, key: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def encrypt_key(self, unprotected_key: bytes) -> str:
        raise NotImplementedError

    @abstractmethod
    def decrypt_key(self, protected_key: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def compare(self, a: str | bytes, b: str | bytes) -> bool:
        raise NotImplementedError


class Auth(AuthInterface):
    """The Authentication class handles encryption/decrytpion/pickling/unpickling/hashing of sensitive data"""

    def __init__(self, session: Optional[Session] = None) -> None:
        self.session = session

    @property
    def master_key(self) -> bytes | None:
        user_id = request.cookies.get('user_id')
        # Cast to int if user_id is not None
        if user_id is not None:
            user_id = int(user_id)
        return self.get_master_key(user_id)
    
    @property
    def backend(self):
        return backends.default_backend()

    def get_master_key(self, user_id:int) -> bytes:
        """Get the master key from the database.
        
        Args:
            user_id (int): The user's id
        
        Returns:
            bytes: The master key
        """
        try:
            key = self.session.query(Master_Key) \
                .filter(Master_Key.user_id == user_id).one()
            return key
        except NoResultFound:
            log.warning("No result's from query, creating new key...")
            self.add_master_key()
            return self.get_master_key()

    def hash_password(self, password: str) -> str:
        """Returns the hashed version of the password and the salt"""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Securely verifies the user's password against the hash using bcrypt

        Args:
            password (str): The entered password
            hashed_password (str): The hashed password from the database

        Returns:
            bool: Whether the password matches or not.
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def generate_key(self) -> bytes:
        """Generate a new encryption key

        Returns:
            bytes: The encryption key
        """
        return Fernet.generate_key()

    def encrypt_str(self, unprotected_str: str, key: bytes) -> str:
        """Encrypt a string

        Args:
            unprotected_str (str): The string to encrypt
            key (bytes): The key to use

        Returns:
            str: The encrypted string
        """
        fernet = Fernet(key=key, backend=self.backend)
        protected_str = fernet.encrypt(unprotected_str.encode('utf-8'))
        return protected_str.decode('utf-8')

    def decrypt_str(self, protected_str: str, key: str) -> str:
        """Decrypt a string

        Args:
            protected_str (str): The encrypted string
            key (str): The decryption key

        Returns:
            str: The unencrypted string
        """
        fernet = Fernet(key=key.encode('utf-8'), backend=self.backend)
        unprotected_str = fernet.decrypt(protected_str.encode('utf-8'))
        return unprotected_str.decode('utf-8')

    def encrypt_key(self, unprotected_key: bytes) -> str:
        """Encrypts a key for storing in the database using the master key

        Args:
            unprotected_key (bytes): The key to encrypt

        Returns:
            str: The encrypted key
        """
        fernet = Fernet(key=self.master_key, backend=self.backend)
        protected_key = fernet.encrypt(unprotected_key)
        return protected_key.decode('utf-8')

    def decrypt_key(self, protected_key: str) -> str:
        """Decrypts a key using the master

        Args:
            protected_key (str): The encrypted key

        Returns:
            str: The decrypted key
        """
        fernet = Fernet(key=self.master_key, backend=self.backend)
        unprotected_key = fernet.decrypt(protected_key.encode('utf-8'))
        return unprotected_key.decode('utf-8')

    def compare(self, a: str | bytes, b: str | bytes) -> bool:
        """Compare's two strings in a way to prevent timing attacks

        Args:
            a (str | bytes): A string or bytes
            b (str | bytes): A string or bytes

        Returns:
            bool: Returns a == b
        """
        return hmac.compare_digest(a, b)