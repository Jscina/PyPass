import eel
from login import Login
from accounts import Accounts

login_handler = Login()
account_handler = Accounts()

eel.init("www")


@eel.expose
def login(username: str, password: str) -> bool:
    """Authenticate the user"""
    return login_handler.login(username, password)


@eel.expose
def store_active_user(email: str) -> None:
    """Store the active users email in memory"""
    account_handler.store_active_user(email)

@eel.expose
def get_name(email: str) -> str:
    name = account_handler.get_users_name(email)
    return name


@eel.expose
def create_account(first_name: str, last_name: str, email: str, password: str) -> bool:
    """Create a new login account"""
    return login_handler.create_new_user(first_name, last_name, email, password)


@eel.expose
def reset_password(password_new: str, email: str) -> bool:
    """Reset the user's password"""
    return login_handler.update_login_credentials(email, password_new)


@eel.expose
def get_security_question(email: str) -> str:
    """Get the user's security question"""
    key = login_handler.get_security_question_id(email)
    return login_handler.get_security_question(key)


@eel.expose
def get_security_answer(email: str, answer: str) -> bool:
    """Get the answer to the user's security question"""
    return login_handler.validate_answer(email, answer)


@eel.expose
def get_account_table() -> list[tuple]:
    '''Get the table from memory'''
    accounts = account_handler.get_accounts()
    return accounts


@eel.expose
def populate_memory_db() -> None:
    """Fills the memory database with the active users accounts"""
    account_handler.add_active_user_accounts()


@eel.expose
def close_memory_database() -> None:
    """Closes the memory database"""
    account_handler.mem_db.close()


@eel.expose
def delete_account(row: int) -> None:
    account_handler.remove_account(row)


@eel.expose
def console_log(phrase) -> None:
    print(phrase)


# Start on the login screen
eel.start("login.html", blocking=False)
