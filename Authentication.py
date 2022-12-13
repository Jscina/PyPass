import codecs, hashlib, pickle, uuid
from os import environ
from typing import Any
from cryptography.fernet import Fernet
from cryptography.hazmat import backends


class Auth:
    """The Authentication class handles encryption/decrytpion/pickling/unpickling/hashing of sensitive data"""
    def __init__(self) -> None:
        self.__master_key: bytes = b'uINeV3FVfyDZ-40LcgGzJ8oy0tO3K5hCXl5xJtDp_Cs=' # Development key DO NOT USE IN PRODUCTION
        #__master_key = str(environ.get("CLIENT_SECRET")).encode() for production
      
    def gen_uuid(self) -> str:
        return str(uuid.uuid4())
    
    def dump(self, obj: Any) -> str:
        return codecs.encode(pickle.dumps(obj), "base64").decode()

    def load(self, obj: str) -> Any:
        return pickle.loads(codecs.decode(obj.encode(), "base64"))

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
        assert self.__master_key is not None
        fernet = Fernet(key = self.__master_key, backend=backends.default_backend())
        protected_key = fernet.encrypt(unprotected_key)
        return protected_key.decode()

    def decrypt_key(self, protected_key: str) -> str:
        assert self.__master_key is not None
        fernet = Fernet(key = self.__master_key, backend=backends.default_backend())
        unprotected_key = fernet.decrypt(protected_key.encode())
        return unprotected_key.decode()
