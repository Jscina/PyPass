from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import bcrypt, hmac
# from os import environ
from cryptography.fernet import Fernet
from cryptography.hazmat import backends


@dataclass(frozen=True, slots=True)
class AbstractAuth(ABC):
    """Abstract base class for the Authentication class."""
    @property
    @abstractmethod
    def master_key(self) -> bytes:
        pass

    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        pass

    @abstractmethod
    def generate_key(self) -> bytes:
        pass

    @abstractmethod
    def encrypt_str(self, unprotected_str: str, key: bytes) -> str:
        pass

    @abstractmethod
    def decrypt_str(self, protected_str: str, key: str) -> str:
        pass

    @abstractmethod
    def encrypt_key(self, unprotected_key: bytes) -> str:
        pass

    @abstractmethod
    def decrypt_key(self, protected_key: str) -> str:       
        pass
    
    @abstractmethod
    def compare(self, a:str | bytes, b:str | bytes) -> bool:
        pass
    
@dataclass(frozen=True, slots=True)
class Auth(AbstractAuth):
    """The Authentication class handles encryption/decrytpion/pickling/unpickling/hashing of sensitive data"""
    _master_key: bytes = b'uINeV3FVfyDZ-40LcgGzJ8oy0tO3K5hCXl5xJtDp_Cs='  # Development key DO NOT USE IN PRODUCTION
    backend: Any = backends.default_backend()
    # _master_key: bytes = str(environ.get("CLIENT_SECRET")).encode() for production

    @property
    def master_key(self):
        return self._master_key

    def hash_password(self, password: str) -> str:
        """Returns the hashed version of the password and the salt"""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def generate_key(self) -> bytes:
        return Fernet.generate_key()

    def encrypt_str(self, unprotected_str: str, key: bytes) -> str:
        fernet = Fernet(key=key, backend=self.backend)
        protected_str = fernet.encrypt(unprotected_str.encode())
        return protected_str.decode()

    def decrypt_str(self, protected_str: str, key: str) -> str:
        fernet = Fernet(key=key.encode(), backend=self.backend)
        unprotected_str = fernet.decrypt(protected_str.encode())
        return unprotected_str.decode()

    def encrypt_key(self, unprotected_key: bytes) -> str:
        fernet = Fernet(key=self.master_key, backend=self.backend)
        protected_key = fernet.encrypt(unprotected_key)
        return protected_key.decode()

    def decrypt_key(self, protected_key: str) -> str:
        fernet = Fernet(key=self.master_key, backend=self.backend)
        unprotected_key = fernet.decrypt(protected_key.encode())
        return unprotected_key.decode()

    def compare(self, a: str | bytes, b: str | bytes) -> bool:
        return hmac.compare_digest(a, b)