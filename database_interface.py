import sqlite3

from typing import Any

class Database:
    def __init__(self, name: str = "db.sqlite") -> None:
        self._db_name = name
        self._conn = sqlite3.connect(self._db_name)
        self._cur = self._conn.cursor()
        
    def __enter__(self):
        return self
    
    def __exit__(self):
        self.close()
    
    @property
    def connection(self):
        return self._conn
    
    @property
    def cursor(self):
        return self._cur
    
    def close(self, commit:bool = True) -> None:
        if commit:
            self.commit()
        self.connection.close()
        
    def commit(self):
        self.connection.commit()
        
    def execute(self, query: str, params: tuple | None = None):
        self.cursor.execute(query, params or ())
    
    def executemany(self, query: str, params: tuple | None = None):
        self.cursor.executemany(query, params or ())
        
    def executemultiple(self, queries: list[str], params: tuple | None = None):
        for query in queries:
            self.execute(query, params)
            
    def fetchall(self) -> list[Any]:
        return self.cursor.fetchall()

    def fetchone(self) -> Any:
        return self.cursor.fetchone()
            
