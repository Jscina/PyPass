import sqlite3, os
from contextlib import closing
from dataclasses import dataclass
from authentication import Auth


@dataclass
class Database:
    db_name = "db.sqlite"
    auth = Auth()

    def init_db(self):
        if os.path.exists(os.path.join(os.getcwd(), "app", self.db_name)):
            return
        
        with closing(sqlite3.connect(self.db_name)) as conn, conn as cur:
            queries = ["""CREATE TABLE users (
                            id INTEGER PRIMARY KEY,
                            username TEXT NOT NULL,
                            password TEXT NOT NULL,
                            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                        );""", """
                        CREATE TABLE accounts (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            account_name TEXT NOT NULL,
                            account_username TEXT NOT NULL,
                            account_password TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users(id)
                        );"""]
            for query in queries:
                cur.execute(query)
            conn.commit()
            
    def fetch_login(self, username:str, password: str):
        with closing(sqlite3.connect(self.db_name)) as conn, conn as cur:
            query = "SELECT * FROM users WHERE username = ? AND password = ?"
            params = (username, self.auth.hash_password(password))
            
            cur.execute(query, params)
            
