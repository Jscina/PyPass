import bcrypt
# from os import environ
from cryptography.fernet import Fernet
from cryptography.hazmat import backends
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Auth:
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

    def decrpyt_str(self, protected_str: str, key: str) -> str:
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

    def login(self, username: str, password: str, accounts: list[tuple]) -> bool:
        for account in accounts:
            if username == account[1] and self.verify_password(password, account[2]):
                return True
        return False
