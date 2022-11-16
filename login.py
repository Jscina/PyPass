from pypass_database import PyPass_Database

class Login:
    """Manage user authentication"""
    def __init__(self) -> None:
        self.db = PyPass_Database()
        
    def get_security_question(self, key: int) -> str:
        """Grabs the security question from the dictionary"""
        security_questions: dict = {
        1:"In what city were you born?",
        2:"What is the name of your favorite pet?",
        3:"What is your mother's maiden name?",
        4:"What high school did you attend?",
        5:"What was the name of your elementary school?",
        6:"What was the make of your first car?",
        7:"What was your favorite food as a child?",
        8:"Where did you meet your spouse?",
        9:"What year was your father (or mother) born?"
        }
        return security_questions[key]
    
    def get_security_question_id(self, email: str) -> int:
        """Returns the security question by email"""
        return self.db.get_security_question_id(email)

    def validate_answer(self, email: str, answer: str) -> bool:
        """Validates the security question answer"""
        if self.db.hash(answer) == self.db.get_security_answer(email):
            return True
        else:
            return False
        
    # Login Method
    def login(self, username: str, password: str) -> bool:
        """Authenticates the user"""
        credentials = self.db.load_login_credentials(username)
        _username: str = credentials[0]
        _password: str = credentials[1]
        
        if username ==  _username and self.db.hash(password) == _password:
            return True
        else:
            return False

    def update_login_credentials(self, email: str, password_new: str) -> bool:
        """Updates the user's password"""
        try:
            self.db.update_password(email, password_new)
            return True
        except Exception:
            return False
        
    def create_new_user(self, first_name: str, last_name: str, email: str, password: str, security_question: int, security_answer:str) -> bool:
        """Create a new user"""
        return self.db.create_login_account(first_name, last_name, email, password, security_question, security_answer)