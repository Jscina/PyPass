import logging

from database import Database, get_database
from flask import (Blueprint, Response, jsonify, redirect, render_template,
                   request, session)

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
    setattr(request, "db", Database())


@index_view.after_request
def after_request(response: Response) -> Response:
    db = get_database()
    db.close()
    return response


@index_view.route('/', methods=['GET'])
def index() -> str:
    return render_template("login.html")


@index_view.route('/home', methods=['GET'])
def home() -> Response | str:
    if session.get("logged_in"):
        return render_template("index.html")
    return redirect("/")


@index_view.route("/add_account", methods=["POST"])
def add_account() -> Response:
    db: Database = getattr(request, "db", None)
    if db is None:
        logger.error("No database found in request context")
        return jsonify({"status": "error", "message": "Internal server error"}), 500
    website = request.form["website"]
    username = request.form["username"]
    password = request.form["password"]
    db.create_account(website, username, password)
    del website, username, password
    return redirect("/home")
