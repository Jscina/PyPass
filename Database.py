import sqlite3, contextlib
from Authentication import Auth
from Accounts import Account
from dataclasses import dataclass
from os import path
from os import getcwd

@dataclass(slots=True)
class Database:
    db_name = "db.sqlite"
    
    def verify_database(self) -> bool:
        if path.exists(path.join(getcwd(), self.db_name)):
            return True
        return False
        
    def generate_database(self) -> None:
        with contextlib.closing(sqlite3.connect(self.db_name)) as conn:
            with conn as curr:
                curr.execute("CREATE TABLE USER_LOGIN (UUID TEXT, USERNAME TEXT, PASSWORD TEXT, SALT TEXT);") \
                    .execute("CREATE TABLE USER_STORED_ACCOUNTS(UUID TEXT, USERNAME TEXT, PASSWORD TEXT, DESCRIPTION TEXT, DATE_ADDED TEXT, KEY TEXT)") \
                    .execute("CREATE TABLE USER_RECOVERY(UUID TEXT, SECURITY_QUESTION TEXT, KEY)")

                
if __name__ == "__main__":
    db = Database()
    if not db.verify_database():
        db.generate_database()
    else:
        print("Database already exists")