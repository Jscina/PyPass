#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Title: Pypass Engine** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Purpose: Handle's user input data involving usernames, passwords, and their encryption.** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Imports needed to run engine:** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pickle
from os import path
from datetime import datetime
from cryptography.fernet import Fernet

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Methods for storing and encrypting the usernames/passwords** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class _File_Manager():
    def __init__(self) -> None:
        # This key is only used for the default login
        self._master_key = self.gen_key()

    # Return the object
    def load(self, file) -> None:
        return pickle.load(file)

    # Dump the object
    def dump(self, obj, file) -> None:
        pickle.dump(obj, file)

    # Return master key

    def get_master(self) -> bytes:
        return self._master_key

    # Generate a new key
    def gen_key(self) -> bytes:
        key = Fernet.generate_key()
        return key

    # Create base files
    def gen_data(self) -> None:
        data = ([self.encrypt("Username", self.get_master())],
                [self.encrypt("Password", self.get_master())],
                [self.get_master()],
                [""],
                [""])
        with open("data.pp", "wb") as file:
            self.dump(data, file)
        del data

    # Dump data
    def dump_data(self, data: tuple) -> None:
        try:
            with open("data.pp", "wb") as file:
                self.dump(data, file)
            del data
        except FileNotFoundError:
            self.gen_data()

    # Load and return data
    def load_data(self) -> tuple:
        try:
            with open("data.pp", "rb") as file:
                data = self.load(file)
            return tuple(data)
        except FileNotFoundError:
            self.gen_data()
            return self.load_data()

    # Encrypt a string and return it
    def encrypt(self, phrase: str, key: bytes) -> bytes:
        crypto = Fernet(key)
        return crypto.encrypt(phrase.encode())

    # Decrypt bytes and return it as a string
    def decrypt(self, phrase: bytes, key: bytes) -> bytes:
        crypto = Fernet(key)
        return str(crypto.decrypt(phrase).decode())
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Methods for logging into the app** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Login_Methods():
    def __init__(self) -> None:
        self._crypter = _File_Manager()

    # Login Method
    def login(self, username: str, password: str) -> bool:
        data = self._crypter.load_data()
        username_list = data[0]
        password_list = data[1]
        keys = data[2]

        if username == self._crypter.decrypt(username_list[0], keys[0]) and password == self._crypter.decrypt(password_list[0], keys[0]):
            logged_in = True
        else:
            logged_in = False
        return logged_in

    def gen_data(self) -> None:
        self._crypter = _File_Manager()
        self._crypter.gen_data()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Methods for adding, removing, and displaying accounts** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Main_Window_Methods():
    def __init__(self) -> None:
        self._crypter = _File_Manager()

    def check_for_accounts(self) -> list:
        item:list = ["None"]
        # If there aren't any accounts show none else call the show accounts method
        if len(self._crypter.load_data()[0]) > 1:
            return self.show_accounts()
        else:
            return item

    def show_accounts(self) -> list:
        data = self._crypter.load_data()
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
                data = _crypter.load_data()
                for li in range(len(data)):
                    data[li].remove(data[li][index])
                _crypter.dump_data(data)

    def add_user(self, username: str, password: str, website: str) -> None:
        _crypter = _File_Manager()
        data = _crypter.load_data()
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
        data: tuple = self._crypter.load_data()
        username: bytes = self._crypter.decrypt(data[0][0], data[2][0])
        password: bytes = self._crypter.decrypt(data[1][0], data[2][0])
        text: str = "Username: " + username + " Password: " + password

        del data, username, password

        return text

    def update_login(self, username_new: str, password_new: str) -> None:
        key: bytes = self._crypter.gen_key()
        username: bytes = self._crypter.encrypt(username_new, key)
        password: bytes = self._crypter.encrypt(password_new, key)
        date: datetime = datetime.now()
        data: tuple = self._crypter.load_data()
        data[0][0], data[1][0], data[2][0], data[3][0], data[4][0] = username, password, key, date.strftime(
            "%x"), [""]
        del username, password, key, date
        self._crypter.dump_data(data)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **General Methods used in all UI's** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class General_Purpose:

    def get_icon_path(self) -> str:
        return path.abspath("locked.ico")

    def _get_data_path(self) -> str:
        return path.abspath("data.pp")

    def check_data_path(self) -> bool:
        if path.exists(self._get_data_path()):
            return True
        else:
            return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Beta Section** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Inputs** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    manage = _File_Manager()
    key: bytes = manage.get_master()
    encrypted_text: bytes = manage.encrypt(phrase = "Happy Campers", key = key)

    test_main_window = Main_Window_Methods()
    test_general_purpose = General_Purpose()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Outputs** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Make sure text is encrypted and decrypted properly
    print(encrypted_text, manage.decrypt(phrase = encrypted_text, key = key))
    
    # Check the type that is returned from method
    print(type(test_main_window.check_for_accounts()))

    # Check the type that is returned from method
    print(type(test_general_purpose.get_icon_path()))




