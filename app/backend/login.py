import logging

from database import Database, get_database
from flask import Blueprint, Response, jsonify, redirect, request, session

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

kwargs = {
    "name": "login_view",
    "import_name": __name__,
    "url_prefix": "/"
}
login_view = Blueprint(**kwargs)


@login_view.before_request
def before_request() -> None:
    setattr(request, "db", Database())


@login_view.after_request
def after_request(response: Response) -> Response:
    db = get_database()
    db.close()
    return response


# Login Section
@login_view.route('/login', methods=['POST'])
def login() -> Response:
    db = get_database()

    username = request.form.get("username")
    password = request.form.get("password")

    login_info = {
        "email": username,
        "username": username,
        "password": password
    }
    if "@" in username:
        login_info["username"] = None
    else:
        login_info["email"] = None

    if db.login(**login_info):
        session["logged_in"] = True
        del username, password, login_info
        return jsonify({"status": "success"})

    del username, password, login_info
    message = "Invalid username or password"
    return jsonify({"status": "error", "message": message})


@login_view.route("/logout", methods=["GET", "POST"])
def logout():
    session["logged_in"] = False
    return redirect("/home")