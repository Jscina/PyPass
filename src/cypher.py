from cryptography.fernet import Fernet
#Do Not Edit This Class In Any Way
#@Author Joshua Scina
#@Version 1.1

class Cypher:
    def __init__(self):
        self.key = self.load_key()

    def load_key(self):
        with open("key.key", "rb") as file:
            key = file.readline()
        file.close()
        return key

    def encrypt_phrase(self, phrase):
        cypher = Fernet(self.key)
        encrypted = cypher.encrypt(phrase.encode())
        return encrypted

    def decrypt_phrase(self, phrase):
        cypher = Fernet(self.key)
        decrypted = cypher.decrypt(phrase)
        return decrypted.decode()
