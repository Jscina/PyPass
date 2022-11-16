from datetime import datetime
from database import Database


class PyPass_Database(Database):
    """Persistant Database for storing information"""

    def __init__(self):
        super(PyPass_Database, self).__init__("db.sqlite")

    # Get the accounts from the database
    def get_accounts(self, email) -> list[str]:
        '''Get the accounts from the database'''
        db_con = super().get_connection()
        cur = db_con.cursor()
        cur.execute(
            "SELECT * FROM CREDENTIAL_STORAGE WHERE EMAIL = ?;", (email,))
        accounts = cur.fetchall()
        cur.close()
        db_con.close()
        return accounts

    # Delete an account
    def del_account(self, row: int, email: str) -> None:
        '''Delete an account'''
        db_con = super().get_connection()
        cur = db_con.cursor()
        accounts: list[tuple] = self.get_accounts(email)
        params = accounts[row]
        query = "DELETE FROM CREDENTIAL_STORAGE WHERE EMAIL = ? AND USERNAME = ? AND PASSWORD = ? AND DESCRIPTION = ? AND DATE = ? AND KEY = ?;"
        cur.execute(query, params)
        cur.close()
        db_con.commit()
        db_con.close()

    def generate_schema(self) -> None:
        '''Create the user database. This generally won't need to be called.'''
        queries = [("CREATE TABLE CREDENTIAL_STORAGE(EMAIL, USERNAME, PASSWORD, DESCRIPTION, DATE, KEY);"),
                   ("CREATE TABLE LOGIN(FIRST_NAME, LAST_NAME, EMAIL, PASSWORD, SECURITY_QUESTION, SECURITY_ANSWER);")]
        db_con = super().get_connection()
        super().generate_schema(db_con, db_con.cursor(), queries)

    # Load the user login from Database
    def load_login_credentials(self, email: str) -> tuple[str, str]:
        '''Load the login credentials for the user'''
        db_con = super().get_connection()
        cur = db_con.cursor()
        cur.execute(
            "SELECT EMAIL, PASSWORD FROM LOGIN WHERE EMAIL = ?;", (email,))
        login = cur.fetchone()
        cur.close()
        db_con.close()
        return login

    def get_name_from_permanent(self, email: str) -> str:
        '''Get the users name'''
        db_con = super().get_connection()
        cur = db_con.cursor()
        cur.execute("SELECT FIRST_NAME, LAST_NAME FROM LOGIN WHERE EMAIL = ?;", (email,))
        name = cur.fetchone()
        return f"{name[0]} {name[1]}"
    
    def get_security_question_id(self, email: str) -> int:
        """Get the user's security question id"""
        db_con = super().get_connection()
        cur = db_con.cursor()
        cur.execute(
            "SELECT SECURITY_QUESTION FROM LOGIN WHERE EMAIL = ?;", (email,))
        question = cur.fetchone()
        cur.close()
        db_con.close()
        return int(question[0])

    def get_security_answer(self, email: str) -> str:
        """Get the user's security question answer"""
        db_con = super().get_connection()
        cur = db_con.cursor()
        cur.execute(
            "SELECT SECURITY_ANSWER FROM LOGIN WHERE EMAIL = ?;", (email,))
        answer = cur.fetchone()
        cur.close()
        db_con.close()
        return answer[0]

    def update_password(self, email: str, password: str) -> None:
        '''Update the user's password'''
        db_con = super().get_connection()
        cur = db_con.cursor()
        cur.execute("UPDATE LOGIN SET PASSWORD = ? WHERE EMAIL = ?;",
                    (super().hash(password), email))
        cur.close()
        db_con.commit()
        db_con.close()

    def create_login_account(self, first_name: str, last_name: str, email: str, password: str, security_question: int, security_answer: str):
        '''Create a new user'''
        params = (first_name, last_name, email, super().hash(
            password), security_question, super().hash(security_answer))
        db_con = super().get_connection()
        cur = db_con.cursor()
        cur.execute("INSERT INTO LOGIN VALUES(?, ?, ?, ?, ?, ?);", params)
        cur.close()
        db_con.commit()
        db_con.close()
        return True

    # Add an account to the Database
    def add_account(self, email: str, username: str, password: str, description: str):
        '''Add a new account'''
        date = datetime.today().strftime("%m/%d/%Y")
        db_con = super().get_connection()
        cur = db_con.cursor()
        query = "INSERT INTO CREDENTIAL_STORAGE VALUES (?, ?, ?, ?, ?, ?);"
        key = super().generate_key()
        protected_password = super().encrypt_str(password, key)
        protected_key = super().encrypt_key(key)
        params = (email, username, protected_password,
                  description, date, protected_key)
        cur.execute(query, params)
        cur.close()
        db_con.commit()
        db_con.close()
