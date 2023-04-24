import logging

from database import Database, get_database
from cipher import Cipher_User
from flask import (Blueprint, Response, jsonify, redirect, render_template,
                   request, session, url_for)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

kwargs = {
    "name": "index_view",
    "import_name": __name__,
    "url_prefix": "/"
}
index_view = Blueprint(**kwargs)


@index_view.before_request
def before_request() -> None:
    cipher = Cipher_User()
    setattr(request, "db", Database(cipher=cipher))


@index_view.after_request
def after_request(response: Response) -> Response:
    db = get_database()
    db.close()
    return response


@index_view.route('/', methods=['GET'])
def root() -> str:
    return render_template("login.html")


@index_view.route('/index', methods=['GET'])
def index() -> str:
    return render_template("index.html")


@index_view.route('/home', methods=['GET'])
def home() -> Response:
    if session.get("logged_in"):
        return redirect('/index')
    return redirect("/")

@index_view.route('/fetch_accounts', methods=['GET'])
def fetch_accounts() -> Response:
    db: Database = getattr(request, "db", None)
    if db is None:
        logger.error("No database found in request context")
        return jsonify({"status": "error", "message": "Internal server error"}), 500
    accounts = db.fetch_accounts(session.get("logged_in"), session.get("user_id"))
    Account = dict[int, dict[str, str]]
    # Reformats the accounts into a dictionary with the account id as the key for javascript to use
    accounts:list[Account] = [{account.id : {"website": account.website, "username": account.username, "password": account.password}} for account in accounts]  
    
    return jsonify(accounts)

@index_view.route("/add_account", methods=["POST"])
def add_account() -> Response:
    db: Database = getattr(request, "db", None)
    if db is None:
        logger.error("No database found in request context")
        return jsonify({"status": "error", "message": "Internal server error"}), 500
    website = request.form["website"]
    username = request.form["username"]
    password = request.form["password"]
    db.add_account(website, username, password)
    del website, username, password
    return redirect("/home")
