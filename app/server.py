from secrets import token_hex
from authentication import Auth
from database import Database
from flask import (Flask, Response,
                   redirect, render_template,
                   request, session,
                   jsonify)

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
# Basic config for the server
server.secret_key = token_hex(16)
server.config["SESSION_COOKIE_SAMESITE"] = "Lax"
server.config["SESSION_COOKIE_SECURE"] = True
server.config["SESSION_COOKIE_HTTPONLY"] = True


# Index section
@server.route('/', methods=['GET'])
def index() -> str:
    return render_template("login.html")


@server.route('/home', methods=['GET'])
def home() -> Response | str:
    print("Hit")
    if bool(session.get("logged_in")):
        return render_template("index.html")
    return redirect("/")


@server.route("/add_account", methods=["POST"])
def add_account() -> Response:
    website = request.form["website"]
    username = request.form["username"]
    password = request.form["password"]
    __db.create_account(website, username, password)
    del website, username, password
    return redirect("/home")


# Login Section
@server.route('/login', methods=['POST'])
def login() -> Response:
    username = request.form.get("username")
    password = request.form.get("password")
    accounts = __db.fetch_login(username)

    if __auth.login(username, password, accounts):
        session["logged_in"] = True
        del username, password, accounts
        return jsonify({"status": "success"})

    del username, password, accounts
    message = "Invalid username or password"
    return jsonify({"status": "error", "message": message})


@server.route("/logout", methods=["GET", "POST"])
def logout():
    session["logged_in"] = False
    return redirect("/home")

# Create Account section
@server.route('/create_account_redirect', methods=['GET', 'POST'])
def create_account_redirect() -> str:
    return render_template("create_account.html")


@server.route('/create_account', methods=['POST'])
def create_account() -> Response:
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    if password != confirm_password:
        message = "Passwords do not match"
        return jsonify({"status": "error", "message": message})

    message = __db.create_user(username, password)

    if isinstance(message, str):
        return jsonify({"status": "error", "message": message})

    del username, password
    return redirect("/home")


# Recover Account section
@server.route('/recover_account', methods=['GET'])
def recover_account():
    return None


# Testing Server
def run_testing_sever() -> None:
    """Run this to debug as a website"""
    server.run(host="localhost", port=5000, debug=True)


if __name__ == "__main__":
    run_testing_sever()
