from dataclasses import dataclass
from typing import Optional, Protocol

import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat import backends


@dataclass(unsafe_hash=True)
class Cipher(Protocol):
    """Protocol class for the Encryption class."""
    @property
    def master_key(self) -> bytes:
        ...

    @master_key.setter
    def master_key(self, key: bytes) -> None:
        ...

    async def hash_password(self, password: str) -> str:
        """Returns the hashed version of the password and the salt"""
        ...
    
    @staticmethod
    async def generate_key() -> bytes:
        """Generate a new encryption key"""
        ...

    async def encrypt(self, unprotected: str | bytes, key: bytes, encrypt_key: bool = False) -> str:
        """Encrypt a string or bytes"""  
        ...

    async def decrypt(self, protected: str | bytes, key: bytes, encrypt_key: bool = False) -> str:
        """Decrypt a string or bytes"""
        ...


@dataclass(unsafe_hash=True)
class Cipher_User:
    """The Encryption class handles encryption/decrytpion//hashing of sensitive data"""
    _master_key: Optional[bytes] = None

    @property
    def master_key(self) -> bytes:
        return self._master_key

    @master_key.setter
    def master_key(self, key: bytes) -> None:
        self.master_key = key

    async def hash_password(self, password: str) -> str:
        """Returns the hashed version of the password and the salt"""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
    
    @staticmethod
    async def generate_key() -> bytes:
        """Generate a new encryption key"""
        return Fernet.generate_key()
    
    async def encrypt(self, unprotected: str | bytes, key: bytes, encrypt_key: bool = False) -> str | tuple[str, str]:
        """Encrypt a string or bytes, if encrypt_key is True, encrypt the key as well"""        
        fernet = Fernet(key=key, backend=backends.default_backend())
        protected_str = fernet.encrypt(unprotected.encode('utf-8'))
        if encrypt_key:
            protected_key = self.encrypt(key.decode("utf-8"), self.master_key)
            return (protected_str.decode('utf-8'), protected_key.encode("utf-8"))
        return protected_str.decode('utf-8')

    async def decrypt(self, protected: str, key: bytes, encrypted_key: bool = False) -> str:
        """Decrypt a string or bytes"""
        if encrypted_key:
            key = self.decrypt(key.decode("utf-8"), self.master_key)
        fernet = Fernet(key=key, backend=backends.default_backend())
        unprotected_str = fernet.decrypt(protected.encode('utf-8'))
        return unprotected_str.decode('utf-8')

    