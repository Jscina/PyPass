from flask import (Blueprint, Response,
                   redirect, render_template,
                   request, session)
from database import Database

db = Database()

kwargs = {
    "name":"index_view",
    "import_name":__name__,
    "url_prefix":"/"
}
index_view = Blueprint(**kwargs)

# Index section
@index_view.route('/', methods=['GET'])
def index() -> str:
    return render_template("login.html")


@index_view.route('/home', methods=['GET'])
def home() -> Response | str:
    if bool(session.get("logged_in")):
        return render_template("index.html")
    return redirect("/")

@index_view.route("/add_account", methods=["POST"])
def add_account() -> Response:
    website = request.form["website"]
    username = request.form["username"]
    password = request.form["password"]
    db.create_account(website, username, password)
    del website, username, password
    return redirect("/home")