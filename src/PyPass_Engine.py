#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Title: Pypass Engine** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Purpose: Library that contains everything the program requires to function** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Imports needed to run engine:** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sqlite3
from os import path, environ
from datetime import datetime
from cryptography.fernet import Fernet

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Methods for storing and encrypting the usernames/passwords** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class _File_Manager():
    def __init__(self) -> None:
        self._master_key:bytes = str(environ.get("PYPASS_SECRET")).encode()

    # Return master key
    def get_master(self) -> bytes:
        return self._master_key

    # Generate a new key
    def gen_key(self) -> bytes:
        key = Fernet.generate_key()
        return key
        
    # Get the keys from the database
    def get_keys(self) -> list:
        db_con = sqlite3.connect("PyPass.db")
        cur = db_con.cursor()
        keys = list()
        try:
            cur.execute("SELECT * FROM KEY_STORAGE;")
            keys = cur.fetchall()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            db_con.close()
            return keys
            
    # Get the accounts from the database
    def get_accounts(self) -> list:
        db_con = sqlite3.connect("PyPass.db")
        cur = db_con.cursor()
        accounts = list()
        try:
            cur.execute("SELECT * FROM CREDENTIAL_STORAGE;")
            accounts = cur.fetchall()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            db_con.close()
            return accounts
        
    def del_account(self, account, key) -> None:
        db_con = sqlite3.connect("PyPass.db")
        cur = db_con.cursor()
        try:
            cur.execute("DELETE FROM CREDENTIAL_STORAGE WHERE USERNAME = ?;", (account,))
            cur.execute("DELETE FROM KEY_STORAGE WHERE KEY = ?;", (key,))
            db_con.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            db_con.close()
            
    # Create database if it doesn't already exist and populate it with default values
    def gen_database(self) -> None:
        key = self.gen_key()
        default_username = self.encrypt("Username", key).decode()
        default_password = self.encrypt("Password", key).decode()
        db_con = sqlite3.connect("PyPass.db")
        cur = db_con.cursor()
        key = self.encrypt(key.decode(), self.get_master()).decode()
        try:
            cur.execute("CREATE TABLE CREDENTIAL_STORAGE(USERNAME, PASSWORD, WEBSITE, DATE);")
            cur.execute("CREATE TABLE KEY_STORAGE(KEY);")
            cur.execute("CREATE TABLE LOGIN(USERNAME, PASSWORD, KEY);")
            cur.execute("INSERT INTO LOGIN VALUES(?, ?, ?);", (default_username, default_password, key))
            db_con.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            db_con.close()    

    # Load the user login from database
    def load_login_credentials(self) -> tuple:
        db_con = sqlite3.connect("PyPass.db")
        cur = db_con.cursor()
        try:
            cur.execute("SELECT * from LOGIN")
            login = cur.fetchall()
            credentials = (login[0][0], login[0][1], login[0][2])
            return credentials
        except Exception as e:
            print(e)
            self.gen_database()
            return self.load_login_credentials()
        finally:
            cur.close()
            db_con.close()
            
    def update_login(self, username: str, password: str, old_key: str, new_key: str) -> None:
        db_con = sqlite3.connect("PyPass.db")
        cur = db_con.cursor()
        key = self.encrypt(new_key, self.get_master()).decode()
        try:
            cur.execute("UPDATE LOGIN SET USERNAME = ?, PASSWORD = ?, KEY = ?;", (username, password, key))
            db_con.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            db_con.close()
    
    def add_account(self, username: bytes, password: bytes, key: bytes, website:str):
        db_con = sqlite3.connect("PyPass.db")
        cur = db_con.cursor()
        date = datetime.today().strftime("%m/%d/%Y")
        try:
            cur.execute("INSERT INTO CREDENTIAL_STORAGE VALUES (?, ?, ?, ?);", (username.decode(), password.decode(), website, date))
            cur.execute("INSERT INTO KEY_STORAGE VALUES (?);", (key.decode(),))
            db_con.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            db_con.close()
                   
    # Encrypt a string and return it
    def encrypt(self, phrase: str, key: bytes) -> bytes:
        crypto = Fernet(key)
        return crypto.encrypt(phrase.encode())

    # Decrypt bytes and return it as a string
    def decrypt(self, phrase: bytes, key: bytes) -> str:
        crypto = Fernet(key)
        return crypto.decrypt(phrase).decode()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Methods for logging into the app** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Login_Methods():
    def __init__(self) -> None:
        self._crypter = _File_Manager()

    # Login Method
    def login(self, username: str = "Username", password: str = "Password") -> bool:
        credentials = self._crypter.load_login_credentials()
        _username: bytes = credentials[0].encode()
        _password:bytes = credentials[1].encode()
        key:bytes = credentials[2].encode()
        key = self._crypter.decrypt(key, self._crypter.get_master()).encode()

        if username == self._crypter.decrypt(_username, key) and password == self._crypter.decrypt(_password, key):
            logged_in = True
        else:
            logged_in = False
        return logged_in

    def gen_database(self) -> None:
        self._crypter.gen_database()   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Methods for adding, removing, and displaying accounts** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Main_Window_Methods():
    def __init__(self) -> None:
        self._crypter = _File_Manager()

    def check_for_accounts(self) -> list:
        accounts = self._crypter.get_accounts()
        # If there aren't any accounts show none else call the show accounts method
        if len(accounts) >= 1:
            return self.show_accounts()
        else:
            return ["None"]

    def show_accounts(self) -> list:
        accounts = self._crypter.get_accounts()
        keys = self._crypter.get_keys()
        accounts_to_show = list()
        for index in range(len(keys)):
            key:str = self._crypter.decrypt(keys[index][0], self._crypter.get_master())
            username = self._crypter.decrypt(accounts[index][0], key.encode())
            password = self._crypter.decrypt(accounts[index][1], key.encode())

            accounts_to_show.append(f"{index + 1} Webiste: {str(accounts[index][2])} Username: {username} Password: {password} Date Added: {accounts[index][3]}")

        if len(keys) < 1:
            del keys, accounts_to_show, accounts
            return ["None"]
        else:
            del keys
            return accounts_to_show

    def remove_accounts(self, account_to_be_removed: int) -> None:
            index = account_to_be_removed
            accounts = self._crypter.get_accounts()
            keys = self._crypter.get_keys()
            account = accounts[index][0]
            key = keys[index][0]
            del accounts, keys
            self._crypter.del_account(account, key)
            self.show_accounts()

    def add_user(self, username: str, password: str, website: str) -> None:
        key = self._crypter.gen_key()
        new_username:bytes = self._crypter.encrypt(username, key)
        new_password:bytes = self._crypter.encrypt(password, key)
        secured_key = self._crypter.encrypt(key.decode(), self._crypter.get_master())
        del username, password, key
        self._crypter.add_account(new_username, new_password, secured_key, website)
        self.show_accounts()
        
        
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Methods for changing app login credentials** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Update_Window_Methods:
    def __init__(self) -> None:
        self._crypter = _File_Manager()
        
    def show_current_login(self) -> str:
        login_credentials = self._crypter.load_login_credentials()
        key:bytes = self._crypter.decrypt(login_credentials[2].encode(), self._crypter.get_master()).encode()
        username = self._crypter.decrypt(login_credentials[0], key)
        password = self._crypter.decrypt(login_credentials[1], key)
        text: str = "Username: " + username + " Password: " + password
        del key, username, password, login_credentials

        return text

    def update_login(self, username_new: str, password_new: str) -> None:
        login_credentials = self._crypter.load_login_credentials()
        old_key = self._crypter.decrypt(login_credentials[2].encode(), self._crypter.get_master())
        new_key: str = self._crypter.gen_key().decode()
        username: str = self._crypter.encrypt(username_new, new_key.encode()).decode()
        password: str = self._crypter.encrypt(password_new, new_key.encode()).decode()
        self._crypter.update_login(username, password, old_key, new_key)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **General Methods used in all UI's** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class General_Purpose:

    def get_icon_path(self) -> str:
        return path.abspath("PyPass.ico")

    def _get_database_path(self) -> str:
        return path.abspath("PyPass.db")

    def check_database_path(self) -> bool:
        if path.exists(self._get_database_path()):
            return True
        else:
            return False


if __name__ == "__main__":
    test_login = Login_Methods()
    test_main_window = Main_Window_Methods()
    print(test_login.login())
    #test_main_window.add_user("Test", "Test", "Test")
    print(test_main_window.show_accounts())    




