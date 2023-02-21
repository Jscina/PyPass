from flask import (Blueprint, Response,
                   jsonify, redirect,
                   render_template, request)

from database import Database

db = Database()
kwargs = {
    "name":"create_account_view",
    "import_name":__name__,
    "url_prefix":"/"
}
create_account_view = Blueprint(**kwargs)

# Create Account section
@create_account_view.route('/create_account_redirect', methods=['GET', 'POST'])
def create_account_redirect() -> str:
    return render_template("create_account.html")


@create_account_view.route('/create_account', methods=['POST'])
def create_account() -> Response:
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    if password != confirm_password:
        message = "Passwords do not match"
        return jsonify({"status": "error", "message": message})

    message = db.create_user(username, password)

    if isinstance(message, str):
        return jsonify({"status": "error", "message": message})

    del username, password
    return redirect("/home")

