import logging

from database import Database, get_database
from cipher import Cipher_User
from flask import Blueprint, Response, jsonify, render_template, request

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

kwargs = {
    "name": "recover_account_view",
    "import_name": __name__,
    "url_prefix": "/"
}

recover_account_view = Blueprint(**kwargs)

@recover_account_view.before_request
def before_request() -> None:
    cipher = Cipher_User()
    setattr(request, "db", Database(cipher=cipher))


@recover_account_view.after_request
def after_request(response: Response) -> Response:
    db = get_database()
    db.close()
    return response

@recover_account_view.route('/recover_account', methods=['GET'])
def recover_account():
    return render_template("recover_account.html")


@recover_account_view.route("/recover", methods=["POST"])
def recover(email: str, password: str, confirm_password: str) -> Response:
    db = get_database()
    if password != confirm_password:
        response = {
            "status": "failure",
            "message": "Passwords do not match"
        }
        return jsonify(response)

    accounts = db.fetch_user(email)
