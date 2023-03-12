from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat import backends


@dataclass
class Cryptography(ABC):
    """Abstract base class for the Encryption class."""
    @property
    @abstractmethod
    def master_key(self) -> bytes:
        raise NotImplementedError

    @master_key.setter
    @abstractmethod
    def master_key(self, key: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    def hash_password(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate_key(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def encrypt(self, unprotected: str | bytes, key: bytes, encrypt_key: bool = False) -> str:
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, protected: str | bytes, key: bytes, encrypt_key: bool = False) -> str:
        raise NotImplementedError


@dataclass
class Cipher_User(Cryptography):
    """The Encryption class handles encryption/decrytpion//hashing of sensitive data"""
    master_key: Optional[bytes] = None

    @property
    def master_key(self) -> bytes:
        return self.master_key

    @master_key.setter
    def master_key(self, key: bytes) -> None:
        self.master_key = key

    def hash_password(self, password: str) -> str:
        """Returns the hashed version of the password and the salt"""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def encrypt(self, unprotected: str | bytes, key: bytes, encrypt_key: bool = False) -> str | tuple[str, str]:
        """Encrypt a string or bytes

        Args:
            unprotected (str | bytes): The string or bytes to encrypt
            key (bytes): The encryption key
            encrypt_key (bool, optional): Whether to encrypt the key. Defaults to False.

        Returns:
            str | tuple[str, str]: The encrypted string or a tuple of the encrypted string and the encrypted key
        """        
        fernet = Fernet(key=key, backend=backends.default_backend())
        protected_str = fernet.encrypt(unprotected.encode('utf-8'))
        if encrypt_key:
            protected_key = self.encrypt(key.decode("utf-8"), self.master_key)
            return (protected_str.decode('utf-8'), protected_key.encode("utf-8"))
        return protected_str.decode('utf-8')

    def decrypt(self, protected: str, key: bytes, encrypted_key: bool = False) -> str:
        """Decrypt a string or bytes

        Args:
            protected (str): The string or bytes to decrypt
            key (bytes): The encryption key
            encrypted_key (bool, optional): Whether the key is encrypted. Defaults to False.

        Returns:
            str: The decrypted string
        """
        if encrypted_key:
            fernet = Fernet(key=self.master_key, backend=backends.default_backend())
            key = fernet.decrypt(key.encode('utf-8'))        
        fernet = Fernet(key=key, backend=backends.default_backend())
        unprotected_str = fernet.decrypt(protected.encode('utf-8'))
        return unprotected_str.decode('utf-8')

    def generate_key(self) -> bytes:
        """Generate a new encryption key

        Returns:
            bytes: The encryption key
        """
        return Fernet.generate_key()
