import eel
from Database import Database
from Accounts import Account

active_user: str | None = None

db = Database()

eel.init("www")


@eel.expose
def login(email:str, password:str):
    print(f"you entered: {email} {password}")


if __name__ == "__main__":
    # Start on the login screen
    eel.start("login.html", blocking=False)
