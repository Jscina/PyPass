import os
from contextlib import closing
from dataclasses import dataclass
from sqlite3 import connect

from authentication import Auth


@dataclass(frozen=True, slots=True)
class Database:
    """PyPass Database interface"""
    db_name: str = "pypass.sqlite"
    auth: Auth = Auth()

    def __post_init__(self) -> None:
        if os.path.exists(os.path.join(os.getcwd(), self.db_name)):
            return

        with closing(connect(self.db_name)) as conn:
            cur = conn.cursor()
            queries = [
                """CREATE TABLE users (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    );""",
                """CREATE TABLE accounts (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            website TEXT NOT NULL,
                            account_name TEXT NOT NULL,
                            account_username TEXT NOT NULL,
                            account_password TEXT NOT NULL,
                            encryption_key TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users(id)
                        );"""]
            for query in queries:
                cur.execute(query)
            conn.commit()

    def create_user(self, username: str, password: str) -> str | None:
        """Creates a new login user

        Args:
            username (str): The username to add
            password (str): The password to add

        Returns:
            str | None: Returns a string if there's an error. Returns nothing if account creation is successful.
        """
        queries = [
            "SELECT * FROM users WHERE username = ?;",
            """INSERT INTO users (
                username,
                password,
                created_at) VALUES(?, ?, datetime());"""
        ]
        hashed_password = self.auth.hash_password(password)
        params = [(username,), (username, hashed_password)]
        del username, password, hashed_password

        with closing(connect(self.db_name)) as conn:
            cur = conn.cursor()
            for param, query in enumerate(queries):
                cur.execute(query, params[param])

                if cur.fetchone():
                    return "Username already exists"
            conn.commit()

    def create_account(self,
                       website: str,
                       username: str,
                       password: str) -> bool:
        query = """INSERT INTO accounts (
                website,
                account_name,
                account_username,
                account_password,
                encryption_key,
                created_at)
        VALUES (?, ?, ?, ?, ?, datetime());"""
        key = self.auth.generate_key()
        protected_password = self.auth.encrypt_str(password, key)
        protected_key = self.auth.encrypt_key(key)
        params = (website, username, protected_password, protected_key)

        del website, username, password, protected_key, protected_password
        with closing(connect(self.db_name)) as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            conn.commit()
        return True

    def fetch_login(self, username: str) -> list[tuple]:
        with closing(connect(self.db_name)) as conn:
            cur = conn.cursor()
            query = "SELECT * FROM users WHERE username = ?;"
            params = (username,)
            cur.execute(query, params)
            accounts: list[tuple] = cur.fetchall()
        return accounts
