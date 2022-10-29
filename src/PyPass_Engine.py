#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Title: Pypass Engine** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Purpose: Handle's user input data involving usernames, passwords, and their encryption.** ######
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
        self._master_key:bytes = environ.get("PYPASS_MASTER").encode()

    # Return master key
    def get_master(self) -> bytes:
        return self._master_key

    # Generate a new key
    def gen_key(self) -> bytes:
        key = Fernet.generate_key()
        return key
        

    def get_keys():
        db_con = sqlite3.connect("PyPass.db")
        cur = db_con.cursor()
        
    # Create database if it doesn't already exist and populate it with default values
    def gen_database(self) -> None:
        default_username = self.encrypt("Username", self.get_master()).decode()
        default_password = self.encrypt("Password", self.get_master()).decode()
        try:
            db_con = sqlite3.connect("PyPass.db")
            cur = db_con.cursor()
            queries = [("CREATE TABLE CREDENTIAL_STORAGE(USERNAME, PASSWORD, WEBSITE, DATE)"),
                    ("CREATE TABLE KEY_STORAGE(KEY)"),
                    ("CREATE TABLE LOGIN(USERNAME, PASSWORD)"),
                    (f"INSERT INTO LOGIN VALUES('{default_username}', '{default_password}')"),
                    (f"INSERT INTO KEY_STORAGE VALUES('{self.get_master().decode()}')")]
            for query in queries:
                cur.execute(query)
            db_con.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            db_con.close()    

    # Load and return data
    def load_database(self) -> tuple:
        try:
            db_con = sqlite3.connect("PyPass.db")
            cur = db_con.cursor()
            cur.execute("SELECT * from LOGIN")
            login = cur.fetchall()
            cur.execute(f"SELECT KEY FROM KEY_STORAGE WHERE KEY = '{self.get_master().decode()}'")
            key = cur.fetchone()
            credentials = (login[0][0], login[0][1], key[0])
            return credentials
        except Exception:
            self.gen_database()
            return self.load_database()
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
        credentials = self._crypter.load_database()
        _username = credentials[0].encode()
        _password = credentials[1].encode()
        key = credentials[2].encode()

        if username == self._crypter.decrypt(_username, key) and password == self._crypter.decrypt(_password, key):
            logged_in = True
        else:
            logged_in = False
        return logged_in

    def gen_database(self) -> None:
        self._crypter = _File_Manager()
        self._crypter.gen_database()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Methods for adding, removing, and displaying accounts** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Main_Window_Methods():
    def __init__(self) -> None:
        self._crypter = _File_Manager()

    def check_for_accounts(self) -> list:
        item:list = ["None"]
        # If there aren't any accounts show none else call the show accounts method
        if len(self._crypter.load_database()[0]) > 1:
            return self.show_accounts()
        else:
            return item

    def show_accounts(self) -> list:
        data = self._crypter.load_database()
        users, passes, keys, accounts = data[0], data[1], data[2], list()

        for index in range(len(keys)):
            fuser, fpass = self._crypter.decrypt(users[index], keys[index]), self._crypter.decrypt(
                passes[index], keys[index])

            if index == 0:
                continue
            else:
                accounts.append(f"{index} Webiste: www.{str(data[4][index])}.com Username: {fuser} Password: {fpass} Date Added: {str(data[3][index])}")

        del users, passes, data
        if len(keys) == 1:
            del keys
            return list(["None"])
        else:
            del keys
            return accounts

    def remove_accounts(self, account_to_be_removed: int) -> None:
            _crypter = _File_Manager()
            index = account_to_be_removed
            if index != 0:
                data = _crypter.load_database()
                for li in range(len(data)):
                    data[li].remove(data[li][index])
                _crypter.dump_data(data)

    def add_user(self, username: str, password: str, website: str) -> None:
        _crypter = _File_Manager()
        data = _crypter.load_database()
        key = _crypter.gen_key()
        date = datetime.now()
        data[0].append(_crypter.encrypt(username, key))
        data[1].append(_crypter.encrypt(password, key))
        data[2].append(key)
        data[3].append(date.strftime("%x"))
        data[4].append(website)
        _crypter.dump_data(data)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Methods for changing app login credentials** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Update_Window_Methods:
    def __init__(self) -> None:
        self._crypter = _File_Manager()

    def show_current_login(self) -> str:
        data: tuple = self._crypter.load_database()
        username: str= self._crypter.decrypt(data[0][0], data[2][0])
        password: str = self._crypter.decrypt(data[1][0], data[2][0])
        text: str = "Username: " + username + " Password: " + password

        del data, username, password

        return text

    def update_login(self, username_new: str, password_new: str) -> None:
        key: bytes = self._crypter.gen_key()
        username: bytes = self._crypter.encrypt(username_new, key)
        password: bytes = self._crypter.encrypt(password_new, key)
        date: datetime = datetime.now()
        data: tuple = self._crypter.load_database()
        data[0][0], data[1][0], data[2][0], data[3][0], data[4][0] = username, password, key, date.strftime(
            "%x"), [""]
        del username, password, key, date
        self._crypter.dump_data(data)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **General Methods used in all UI's** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class General_Purpose:

    def get_icon_path(self) -> str:
        return path.abspath("PyPass.ico")

    def _get_data_path(self) -> str:
        return path.abspath("data.pypass")

    def check_data_path(self) -> bool:
        if path.exists(self._get_data_path()):
            return True
        else:
            return False


if __name__ == "__main__":
    test_login = Login_Methods()
    print(test_login.login())    




