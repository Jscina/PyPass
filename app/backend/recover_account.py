from flask import Blueprint, render_template, jsonify, Response
from database import Database

kwargs = {
    "name":"recover_account_view",
    "import_name":__name__,
    "url_prefix":"/"
}

recover_account_view = Blueprint(**kwargs)
db = Database()
# Recover Account section
@recover_account_view.route('/recover_account', methods=['GET'])
def recover_account():
    return render_template("recover_account.html")

@recover_account_view.route("/recover", methods=["POST"])
def recover(email:str, password:str, confirm_password:str) -> Response:
    if password != confirm_password:
        response = {
            "status":"failure",
            "message":"Passwords do not match"
        }
        return jsonify(response)
    
    accounts = db.fetch_login(email)