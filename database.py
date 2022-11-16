import sqlite3
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat import backends
from os import environ


class Database:
    """Base Database Class"""

    def __init__(self, name) -> None:
        self._db_name = name
        self._master = environ.get("CLIENT_SECRET")

    def get_connection(self):
        return sqlite3.connect(self._db_name)

    def generate_schema(self, db_con: sqlite3.Connection, cur: sqlite3.Cursor, queries: list[str], close=True):
        """Create the table schema"""
        self.execute_many(db_con, cur, queries)
        if close:
            cur.close()
            db_con.close()

    def execute_many(self, db_con: sqlite3.Connection, cur: sqlite3.Cursor, queries: list[str], params: list[tuple] = []):
        """Execute multiple queries"""
        for query in queries:
            cur.execute(query, params)
        db_con.commit()

    def hash(self, password: str):
        """Hash a  password"""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def generate_key(self) -> bytes:
        """Generate an encryption key"""
        return Fernet.generate_key()

    def encrypt_str(self, unprotected_str: str, key: bytes) -> str:
        """Encrypt a string"""
        fernet = Fernet(key=key, backend=backends.default_backend())
        protected_str = fernet.encrypt(unprotected_str.encode())
        return protected_str.decode()

    def decrpyt_str(self, protected_str: str, key: str) -> str:
        """Decrypt a string"""
        fernet = Fernet(key=key.encode(), backend=backends.default_backend())
        unprotected_str = fernet.decrypt(protected_str.encode())
        return unprotected_str.decode()

    def encrypt_key(self, unprotected_key: bytes) -> str:
        """Encrypt a key"""
        fernet = Fernet(key=self._master, backend=backends.default_backend())
        protected_key = fernet.encrypt(unprotected_key)
        return protected_key.decode()

    def decrypt_key(self, protected_key: str) -> str:
        """Decrypt a key"""
        fernet = Fernet(key=self._master, backend=backends.default_backend())
        unprotected_key = fernet.decrypt(protected_key.encode())
        return unprotected_key.decode()
