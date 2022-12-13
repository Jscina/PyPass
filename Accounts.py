from Authentication import Auth

class Account:
    """Stores User Account information"""
    __slots__ = "__uname", "__pword", "__desc", "__key", "__auth"
    def __init__(self, uname: str | None = None, pword: str | None = None, desc: str | None = None, key: str | None = None) -> None:
        self.__uname: str | None = uname
        self.__pword: str | None = pword
        self.__desc: str | None = desc
        self.__key: str | None = key
        self.__auth = Auth()
        
    @property
    def username(self):
        return self.__uname
    
    @property
    def password(self):
        assert self.__key is not None
        assert self.__pword is not None
        return self.__auth.decrpyt_str(self.__pword, self.key)

    @property
    def description(self):
        return self.__desc
    
    @property
    def key(self):
        assert self.__key is not None
        return self.__auth.decrypt_key(self.__key)
        