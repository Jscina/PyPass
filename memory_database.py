from datetime import datetime
from database import Database


class Memory_Database(Database):
    """Transient Database for tracking the active users information"""

    def __init__(self):
        super(Memory_Database, self).__init__(":memory:")
        self._connection = super().get_connection()
        self._cursor = self._connection.cursor()
        self.generate_schema()

    def generate_schema(self):
        '''Generates the memory database and intializes the tables'''
        queries = [("CREATE TABLE ACTIVE_USER(EMAIL);"),
                   ("CREATE TABLE USER_ACCOUNTS(USERNAME, PASSWORD, DESCRIPTION, DATE);")]
        super().generate_schema(self._connection, self._cursor, queries, False)

    def get_active_user_accounts(self) -> list[tuple]:
        '''Returns all the account inside User Accounts'''
        query = "SELECT * FROM USER_ACCOUNTS;"
        self._cursor.execute(query)
        accounts = self._cursor.fetchall()
        return accounts

    def add_active_user(self, email: str):
        '''Stores the active users email'''
        query = "INSERT INTO ACTIVE_USER VALUES(?);"
        param = (email,)
        self._cursor.execute(query, param)
        self._connection.commit()

    def add_active_user_accounts(self, accounts: list[tuple]):
        '''Fills the User Accounts table with the decrypted accounts'''
        for index, account in enumerate(accounts):
            account = list(account)
            protected_key = account[5]
            protected_password = account[2]
            unprotected_key = super().decrypt_key(protected_key)
            unprotected_password = super().decrpyt_str(protected_password, unprotected_key)
            account[2] = unprotected_password
            accounts[index] = tuple(account[1:5])
        query = "INSERT INTO USER_ACCOUNTS VALUES(?, ?, ?, ?);"
        self._cursor.executemany(query, accounts)
        self._connection.commit()

    def add_account(self, username, password, description):
        '''Add a singular user account.'''
        date = datetime.today().strftime("%M/%D/%Y")
        query = "INSERT INTO USER_ACCOUNTS VALUES(?, ?, ?, ?)"
        params = (username, password, description, date)
        self._cursor.execute(query, params)
        self._connection.commit()

    def get_active_user(self) -> str:
        '''Returns the active user's email'''
        query = "SELECT * FROM ACTIVE_USER;"
        self._cursor.execute(query)
        active_user = self._cursor.fetchone()
        return active_user[0]

    def del_account(self, row: int) -> None:
        """Delete an account"""
        query = "SELECT * FROM USER_ACCOUNTS;"
        self._cursor.execute(query)
        accounts = self._cursor.fetchall()
        account_to_delete = accounts[row]
        query = "DELETE FROM USER_ACCOUNTS WHERE USERNAME = ? AND PASSWORD = ? AND DESCRIPTION = ? AND DATE = ?;"
        params = (account_to_delete[0], account_to_delete[1],
                  account_to_delete[2], account_to_delete[3])
        self._cursor.execute(query, params)
        self._connection.commit()

    def close(self):
        '''Close the Database'''
        self._cursor.close()
        self._connection.close()


if __name__ == "__main__":
    from pypass_database import PyPass_Database

    pypass_db = PyPass_Database()
    memory_db = Memory_Database()
    email = "example@example.com"

    accounts = pypass_db.get_accounts(email)
    memory_db.add_active_user_accounts(accounts)
    print(memory_db.get_active_user_accounts())
    memory_db.close()

    for index in range(1, 10):
        pypass_db.del_account(f"Test:{index}")
