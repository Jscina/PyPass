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
        file = open("key.key", "wb")
        key = Fernet.generate_key()
        pickle.dump(key, file)
        file.close()

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

    def encrypt(self, phrase: str):
        crypto = Fernet(self.load_key())
        return crypto.encrypt(phrase.encode())

    # Decrypt bytes and return it as a string
    def decrypt(self, phrase: bytes):
        crypto = Fernet(self.load_key())
        return crypto.decrypt(phrase).decode()
