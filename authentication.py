from cryptography.fernet import Fernet
from cryptography.hazmat import backends
from os import environ
import hashlib


class Authentication:
    def __init__(self) -> None:
        self._master_key: bytes = str(environ.get("CLIENT_SECRET")).encode()
    
    @property
    def master_key(self) -> bytes:
        return self._master_key
    
    def hash(self, password: str) -> str:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def generate_key(self) -> bytes:
        return Fernet.generate_key()

    def encrypt_str(self, unprotected_str: str, key: bytes) -> str:
        fernet = Fernet(key=key, backend=backends.default_backend())
        protected_str = fernet.encrypt(unprotected_str.encode())
        return protected_str.decode()

    def decrpyt_str(self, protected_str: str, key: str) -> str:
        fernet = Fernet(key=key.encode(), backend=backends.default_backend())
        unprotected_str = fernet.decrypt(protected_str.encode())
        return unprotected_str.decode()

    def encrypt_key(self, unprotected_key: bytes) -> str:
        fernet = Fernet(key = self.master_key, backend=backends.default_backend())
        protected_key = fernet.encrypt(unprotected_key)
        return protected_key.decode()

    def decrypt_key(self, protected_key: str) -> str:
        fernet = Fernet(key = self.master_key, backend=backends.default_backend())
        unprotected_key = fernet.decrypt(protected_key.encode())
        return unprotected_key.decode()