import hmac, logging, bcrypt
from abc import ABC, abstractmethod
from flask import request
from dataclasses import dataclass
from cipher import Cipher_User

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

log = logging.getLogger(__name__)

@dataclass
class Authorizer(ABC):
    """Abstract base class for the Authorizing users."""
    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def verify_username(self, a: str | bytes, b: str | bytes) -> bool:
        raise NotImplementedError

@dataclass
class Auththorizer_User(Authorizer):
    """The Authentication class handles authentication of users"""
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Securely verifies the user's password against the hash using bcrypt

        Args:
            password (str): The entered password
            hashed_password (str): The hashed password from the database

        Returns:
            bool: Whether the password matches or not.
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def verify_username(self, a: str | bytes, b: str | bytes) -> bool:
        """Compare's two strings in a way to prevent timing attacks

        Args:
            a (str | bytes): A string or bytes
            b (str | bytes): A string or bytes

        Returns:
            bool: Returns a == b
        """
        return hmac.compare_digest(a, b)