from Authentication import Auth
from dataclasses import dataclass

@dataclass
class Account:
    """Stores User Account information"""
    __uname: str
    __pword: str
    __desc: str
    __key: str
    __auth = Auth()
        
    @property
    def username(self):
        return self.__uname
    
    @property
    def password(self):
        return self.__auth.decrpyt_str(self.__pword, self.key)

    @property
    def description(self):
        return self.__desc
    
    @property
    def key(self):
        return self.__auth.decrypt_key(self.__key)
        