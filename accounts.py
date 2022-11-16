from memory_database import Memory_Database
from pypass_database import PyPass_Database


class Accounts:
    '''Manage user's accounts'''

    def __init__(self) -> None:
        self.mem_db = Memory_Database()
        self.pypass_db = PyPass_Database()

    def store_active_user(self, email):
        '''Store the active user in the memory database'''
        self.mem_db.add_active_user(email)

    def add_active_user_accounts(self) -> None:
        '''Adds the active user's accounts to the memory database'''
        email = self.mem_db.get_active_user()
        accounts = self.pypass_db.get_accounts(email)
        self.mem_db.add_active_user_accounts(accounts)

    def delete_from_memory(self, row: int) -> None:
        '''Delete users account from temporary storage'''
        self.mem_db.del_account(row)

    def delete_from_permanent(self, row: int, email: str) -> None:
        '''Delete user account from permanent storage'''
        self.pypass_db.del_account(row, email)
        
    def get_users_name(self, email: str) -> str:
        '''Get user's name'''
        return self.pypass_db.get_name_from_permanent(email)

    def remove_account(self, row: int) -> None:
        '''Delete a user's account from the database'''
        email = self.mem_db.get_active_user()
        self.delete_from_memory(row)
        self.delete_from_permanent(row, email)

    def get_accounts(self) -> list[tuple]:
        """Get the user accounts from the memory database"""
        return self.mem_db.get_active_user_accounts()

    def add_account(self, username: str, password: str, description: str) -> None:
        '''Adds an account to the database'''
        email = self.mem_db.get_active_user()
        self.pypass_db.add_account(email, username, password, description)
        self.mem_db.add_account(username, password, description)

    def get_active_user(self) -> str:
        return self.mem_db.get_active_user()
