from secrets import token_hex

from flask import Flask

from backend.create_account import create_account_view
from backend.index import index_view
from backend.login import login_view
from backend.recover_account import recover_account_view

# Setup up the Flask server
server_args = {
    "import_name": __name__,
    "static_url_path": "",
    "static_folder": "static",
    "template_folder": "templates"
}
server = Flask(**server_args)
# Basic config for the server
server.secret_key = token_hex(16)
server.config["SESSION_COOKIE_SAMESITE"] = "Lax"
server.config["SESSION_COOKIE_SECURE"] = True
server.config["SESSION_COOKIE_HTTPONLY"] = True

views = (
    index_view,
    create_account_view,
    login_view,
    recover_account_view
)
for view in views:
    server.register_blueprint(view)

# Testing Server


def run_testing_sever() -> None:
    """Run this to debug as a website"""
    server.run(host="localhost", port=5000, debug=True)


if __name__ == "__main__":
    run_testing_sever()
