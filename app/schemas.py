from pydantic import BaseModel, EmailStr

class LoginData(BaseModel):
    username: str = None
    email: EmailStr = None
    password: str

class UserData(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str