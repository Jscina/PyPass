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

from cryptography.fernet import Fernet

class File_Manager():
    def __init__(self):
        # This key is only used for the default login
        self._master_key = self.gen_key()

    # Return the object
    def load(self, file):
        return pickle.load(file)

    # Dump the object
    def dump(self, obj, file):
        pickle.dump(obj, file)

    # Return master key

    def get_master(self):
        return self._master_key

    # Generate a new key
    def gen_key(self):
        key = Fernet.generate_key()
        return key

    # Create base files

    def gen_data(self):
        data = ([self.encrypt("Username", self.get_master())],
                [self.encrypt("Password", self.get_master())],
                [self.get_master()],
                [""],
                [""])
        with open("data.pp", "wb") as file:
            self.dump(data, file)
        del data

    # Dump data
    def dump_data(self, data: tuple):
        try:
            with open("data.pp", "wb") as file:
                self.dump(data, file)
            del data
        except FileNotFoundError:
            self.gen_data()

    # Load and return data
    def load_data(self):
        try:
            with open("data.pp", "rb") as file:
                data = self.load(file)
            return tuple(data)
        except FileNotFoundError:
            self.gen_data()
            return self.load_data()

    # Encrypt a string and return it
    def encrypt(self, phrase: str, key: bytes):
        crypto = Fernet(key)
        return crypto.encrypt(phrase.encode())

    # Decrypt bytes and return it as a string
    def decrypt(self, phrase: bytes, key: bytes):
        crypto = Fernet(key)
        return str(crypto.decrypt(phrase).decode())

class LoginMethods():
    # Login Method
    def login(self, username: str, password: str):
        _crypter = File_Manager()
        data = _crypter.load_data()
        username_list = data[0]
        password_list = data[1]
        keys = data[2]

        if username == _crypter.decrypt(username_list[0], keys[0]) and password == _crypter.decrypt(password_list[0], keys[0]):
            logged_in = True
        else:
            logged_in = False

        return logged_in

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Beta Section** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Inputs** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    manage = File_Manager()
    key: bytes = manage.get_master()
    encrypted_text: bytes = manage.encrypt(phrase = input("Enter text: "), key = key)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Outputs** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    print(encrypted_text, manage.decrypt(phrase = encrypted_text, key = key))




