from flask import Blueprint, Response, jsonify, redirect, request, session

from authentication import Auth
from database import Database

db = Database()
auth = Auth()
kwargs = {
    "name":"login_view",
    "import_name":__name__,
    "url_prefix":"/"
}
login_view = Blueprint(**kwargs)

# Login Section
@login_view.route('/login', methods=['POST'])
def login() -> Response:
    username = request.form.get("username")
    password = request.form.get("password")
    accounts = db.fetch_login(username)

    if auth.login(username, password, accounts):
        session["logged_in"] = True
        del username, password, accounts
        return jsonify({"status": "success"})

    del username, password, accounts
    message = "Invalid username or password"
    return jsonify({"status": "error", "message": message})


@login_view.route("/logout", methods=["GET", "POST"])
def logout():
    session["logged_in"] = False
    return redirect("/home")