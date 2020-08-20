from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

# Do Not Edit This Class In Any Way
# @Author Joshua Scina
# @Version 1.1


class Cypher:
    def __init__(self):
        self.key = self.load_key()

    # This function runs if key.key and login.txt doesn't exist
    def gen_files(self):
        # Generates the login file if not present
        # Returns the decrypted login credentials
        acc = self.get_username_password()
        # Reencrypts with the new key
        with open("login.txt", "wb") as file:
            file.write(
                self.encrypt_phrase(acc[0]) + b"\n" + self.encrypt_phrase(acc[1])
            )

    def load_key(self):
        try:
            with open("key.key", "rb") as file:
                key = file.readline()
            return key
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open("key.key", "wb") as file:
                file.write(key)
            return self.load_key()

    # Gets the current login credentials and returns them as a list
    def get_username_password(self):
        try:
            with open("login.txt", "rb") as file:
                acc = file.readlines()
            acc_new = [
                str(self.decrypt_phrase(acc[0])),
                str(self.decrypt_phrase(acc[1])),
            ]
            return acc_new
        except FileNotFoundError:
            with open("login.txt", "wb") as file:
                file.write(
                    self.encrypt_phrase("username")
                    + b"\n"
                    + self.encrypt_phrase("password")
                )
            return self.get_username_password()

    def encrypt_phrase(self, phrase):
        cypher = Fernet(self.load_key())
        encrypted = cypher.encrypt(phrase.encode())
        return encrypted

    def decrypt_phrase(self, phrase):
        cypher = Fernet(self.load_key())
        decrypted = cypher.decrypt(phrase)
        return decrypted.decode()
