import logging

from database import Database, get_database
from cipher import Cipher_User
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
    cipher = Cipher_User()
    setattr(request, "db", Database(cipher=cipher))


@login_view.after_request
def after_request(response: Response) -> Response:
    db = get_database()
    db.close()
    return response

# Login Section
@login_view.route('/login', methods=['POST'])
def login() -> Response:
    db = get_database()

    username_or_email = request.form.get("username")
    password = request.form.get("password")

    login_info = {
        "email": username_or_email,
        "username": username_or_email,
        "password": password
    }

    if "@" in username_or_email:
        login_info["username"] = None
    else:
        login_info["email"] = None
    try:
        login = db.login(**login_info)
    except ValueError as e:
        return jsonify({"status": "error", "message": f"{e}"})

    if isinstance(login, bool) and not login:
        return jsonify({"status": "error", "message": "Invalid username or password"})
    assert isinstance(login, tuple), f"Expected tuple, got {type(login)}"
    logged_in, user = login

    if logged_in:
        session["logged_in"] = True
        response = jsonify({"status": "success"})
        response.set_cookie("user_id", str(user.id), secure=True, samesite="Strict")
        del username_or_email, password, login_info
        return response

    del username_or_email, password, login_info
    message = "Invalid username or password"
    return jsonify({"status": "error", "message": message})


@login_view.route("/logout", methods=["GET", "POST"])
def logout():
    session["logged_in"] = False
    return redirect("/home")
