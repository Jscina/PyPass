import secrets
from dataclasses import dataclass

from database import Database
from authentication import Auth
from flask import Flask, redirect, render_template, request, session, jsonify
from threading import Thread

@dataclass
class Server:
    name: str
    db: Database = Database()
    auth: Auth = Auth()

    def __post_init__(self):
        self.app = Flask(self.name, static_url_path="", static_folder="static", template_folder="templates")
        self.app.secret_key = secrets.token_hex(16)
        self._error_message = ""
        for endpoint in self.endpoints:
            self.add_endpoint(**endpoint)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    @property
    def endpoints(self) -> list[dict]:
        return self.__get_endpoints()
    
    @property
    def error_message(self) -> str:
        return self._error_message
    
    @error_message.__setattr__
    def set_error_message(self, message:str):
        self._error_message = message
        
    def __get_endpoints(self) -> list[dict]:
        endpoints = [
            {
                'endpoint': '/',
                'endpoint_name': 'index',
                'handler': self.index,
                'methods': ['GET']
            },
            {
                'endpoint': '/login',
                'endpoint_name': 'login',
                'handler': self.login,
                'methods': ['POST']
            },
            {
                'endpoint': '/create_account_redirect',
                'endpoint_name': 'create_account_redirect',
                'handler': self.create_account_redirect,
                'methods': ['GET']
            },
            {
                'endpoint': '/create_account',
                'endpoint_name': 'create_account',
                'handler': self.create_account,
                'methods': ['POST']    
            },
            {
                'endpoint': '/recover_account',
                'endpoint_name': 'recover_account',
                'handler': self.recover_account,
                'methods': ['GET']
            },
            {
                'endpoint': '/home',
                'endpoint_name': 'home',
                'handler': self.home,
                'methods': ['GET']
            },
            {
                'endpoint': '/get_error_message',
                'endpoint_name': 'get_error_message',
                'handler': self.get_error_message,
                'methods': ['GET']
            }
            
        ]
        return endpoints

    def get_error_message(self):
        error_msg = {"message":self.message}
        return jsonify(error_msg)
    
    
    def index(self):
        return render_template("login.html")

    def login(self):
        username = request.form["username"]
        password = request.form["password"]
        
        accounts = self.db.fetch_login(username)
        
        if self.auth.login(username, password, accounts):
            session["logged_in"] = True
            del username, password, accounts
            return redirect("/home")
        else:
            del username, password, accounts
            message = "Invalid username or password"
            return render_template("login.html", message = message)

    def create_account_redirect(self):
        return render_template("create_account.html")

    def create_account(self):
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        if password != confirm_password:
            self.error_message = "Passwords do not match"
        
        message = self.db.create_user(username, password)
        
        if isinstance(message, str):
            self.error_message = message
            
        del username, password
        
        return redirect("/home")

    def recover_account(self):
        return None

    def home(self):
        if "logged_in" in session:
            return render_template("index.html", name="Josh!")
        return redirect("/")

    def run_testing_sever(self):
        self.app.run(host= "localhost", port = 5000, debug = True)
        
    def run_server(self,  host: str = "localhost", port: int = 5000, debug: bool = False) -> None:
        server = Thread(target=self.app.run, args=((host, port, debug)), daemon=True)
        server.start()
