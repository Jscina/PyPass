from cryptography.fernet import Fernet
import pickle

# @Author: Joshua Scina
# @Version: 2.0


class File_Manager:
    # Return the object
    def load(self, file):
        return pickle.load(file)

    # Dump the object
    def dump(self, obj, file):
        pickle.dump(obj, file)

    # Create new key if one doesn't exist
    def gen_key(self):
        with open("key.key", "wb") as file:
            key = Fernet.generate_key()
            self.dump(key, file)
        del key

    # Load and return key and call the gen_key() method if the file doesn't exist then re-invoke the method
    def load_key(self):
        try:
            with open("key.key", "rb") as file:
                key = pickle.load(file)
            return key
        except FileNotFoundError:
            self.gen_key()
            return self.load_key()

    # Encrypt a string and return it
    def encrypt(self, phrase: str, key: bytes):
        crypto = Fernet(key)
        return crypto.encrypt(phrase.encode())

    # Decrypt bytes and return it as a string
    def decrypt(self, phrase: bytes, key: bytes):
        crypto = Fernet(key)
        return crypto.decrypt(phrase).decode()

    # Generate an empty dictionary with 3 keys
    def generate_base_dict(self, keys: list = [], usernames: list = []):
        temp = list()
        for index in range(len(usernames)):
            keys.append(Fernet.generate_key())
        for user in range(len(usernames)):
            temp.append(self.encrypt(usernames[user], keys[user]))
        base_dict = dict.fromkeys(temp)
        del temp, usernames
        return base_dict, keys

    # Encrypts the dictionary using generated keys
    def dict_encrypt(self, base_dict: dict, passwords: list, index: int = 0, keys: list = []):

        for key in base_dict.keys():
            keys.append(Fernet.generate_key())
            base_dict.update({key: self.encrypt(passwords[index], keys[index])})
            index += 1

        with open("key.key", "wb") as file:
            self.dump(keys, file)
        del passwords, index, keys
        return base_dict

    # Decrypts the dictionary using it's keys
    def dict_decrypt(self, loaded_dict: dict):
        usernames = list(loaded_dict.keys())
        passwords = list(loaded_dict.values())

        with open("key.key", "rb") as file:
            keys = self.load(file)

        accounts = list()

        for index in range(len(usernames)):
            accounts.append("Username: ", self.decrypt(usernames[index], keys[index]),"Password: ", self.decrypt(passwords[index], keys[index]))
        del usernames, passwords, keys
        return accounts
        