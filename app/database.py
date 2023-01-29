import sqlite3, os
from contextlib import closing
from dataclasses import dataclass
from authentication import Auth


@dataclass(frozen=True, slots=True)
class Database:
    db_name = "pypass.sqlite"
    auth = Auth()

    def init_db(self) -> None:
        if os.path.exists(os.path.join(os.getcwd(), self.db_name)):
            return
        
        with closing(sqlite3.connect(self.db_name)) as conn, conn as cur:
            cur = cur.cursor()
            queries = ["""CREATE TABLE users (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        salt TEXT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    );""", 
                        """CREATE TABLE accounts (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER NOT NULL,
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
            
    def create_user(self, username:str, password:str) -> None:
        query = "INSERT INTO users (username, password, salt, created_at) VALUES(?, ?, ? , datetime())"
        hashed_password, salt = self.auth.hash_password(password)
        params = (username, hashed_password, salt)
        
        del username, password, hashed_password, salt
        
        with closing(sqlite3.connect(self.db_name)) as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            conn.commit()
    
    def create_account(self, username:str, password:str) -> None:
        query = "INSERT INTO accounts (account_name, account_username, account_password, encryption_key, created_at) VALUES (?, ?, ?, ?, datetime());"
        key = self.auth.generate_key()
        protected_password = self.auth.encrypt_str(password, key)
        protected_key = self.auth.encrypt_key(key)
        params = (username, protected_password, protected_key)
        
        del username, password, protected_key, protected_password
        
        with closing(sqlite3.connect(self.db_name)) as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            conn.commit()
            
    def fetch_login(self, username:str) -> list[tuple]:
        with closing(sqlite3.connect(self.db_name)) as conn:
            cur = conn.cursor()
            query = "SELECT * FROM users WHERE username = ?;"
            params = (username,)
            
            cur.execute(query, params)
            accounts:list[tuple] = cur.fetch_all()
            
        return accounts
            
            
if __name__ == "__main__":
    db = Database()
    db.init_db()