from flask import (Blueprint, Response,
                   jsonify, redirect,
                   render_template, request)

from database import Database, get_database
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

kwargs = {
    "name": "create_account_view",
    "import_name": __name__,
    "url_prefix": "/"
}
create_account_view = Blueprint(**kwargs)

@create_account_view.before_request
def before_request() -> None:
    setattr(request, "db", Database())


@create_account_view.after_request
def after_request(response: Response) -> Response:
    db = get_database()
    db.close()
    return response

# Create Account section
@create_account_view.route('/create_account_redirect', methods=['GET', 'POST'])
def create_account_redirect() -> str:
    return render_template("create_account.html")

@create_account_view.route('/create_account', methods=['POST'])
def create_account() -> Response:
    db = get_database()
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    confirm_password = request.form.get("confirm_password")
    if password != confirm_password:
        message = "Passwords do not match"
        return jsonify({"status": "error", "message": message})
    message = db.create_user(email, username, password)

    if isinstance(message, str):
        return jsonify({"status": "error", "message": message})

    del username, password
    return redirect("/home")
