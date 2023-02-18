from functools import wraps
import json
import webview
from secrets import token_hex
from authentication import Auth
from database import Database
from flask import (Flask, redirect,
                   render_template,
                   request, session,
                   Response)

# Initalize the database
__db: Database = Database()
# Initalize the authentication client
__auth: Auth = Auth()
# Setup up the Flask server
__server_args = {
    "import_name": __name__,
    "static_url_path": "",
    "static_folder": "static",
    "template_folder": "templates"
}
server = Flask(**__server_args)
server.secret_key = token_hex(16)


# Token verification
def verify_token(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        data = json.loads(request.data)
        token = data.get("token")
        if token == webview.token:
            return function(*args, **kwargs)
        else:
            raise Exception("Authentication Error")
    return wrapper


# Index section
@server.route('/', methods=['GET'])
def index() -> str:
    return render_template("login.html")


@server.route('/home', methods=['GET'])
@verify_token
def home() -> Response:
    if "logged_in" in session:
        return render_template("index.html")
    return redirect("/")


@server.route("/add_account", methods=["POST"])
@verify_token
def add_account() -> Response:
    website = request.form["website"]
    username = request.form["username"]
    password = request.form["password"]
    __db.create_account(website, username, password)
    del website, username, password
    return redirect("/home")


# Login Section
@server.route('/', methods=['POST'])
@verify_token
def login() -> str | Response:
    username = request.form["username"]
    password = request.form["password"]

    accounts = __db.fetch_login(username)

    if __auth.login(username, password, accounts):
        session["logged_in"] = True
        del username, password, accounts
        return redirect("/home")
    else:
        del username, password, accounts
        message = "Invalid username or password"
        return render_template("login.html", message=message)


# Create Account section
@server.route('/create_account_redirect', methods=['GET'])
@verify_token
def create_account_redirect() -> str:
    return render_template("create_account.html")


@server.route('/create_account', methods=['POST'])
@verify_token
def create_account() -> Response:
    username = request.form["username"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if password != confirm_password:
        message = "Passwords do not match"

    message = __db.create_user(username, password)

    if isinstance(message, str):
        message = message

    del username, password
    return redirect("/home")


# Recover Account section
@server.route('/recover_account', methods=['GET'])
@verify_token
def recover_account():
    return None


# Testing Server
def run_testing_sever() -> None:
    """Run this to debug as a website"""
    server.run(host="localhost", port=5000, debug=True)


if __name__ == "__main__":
    run_testing_sever()
