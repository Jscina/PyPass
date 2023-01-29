from __future__ import annotations
from flask import Flask, redirect, render_template, request, session
from authentication import Auth
from database import Database
import secrets, os

app = Flask(__name__, static_url_path = "", static_folder = "static", template_folder = "templates")
app.secret_key = secrets.token_hex(16)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if username == "admin" and password == "admin":
        session["logged_in"] = True
        return redirect("/home")
    else:
        message = "Invalid username or password"
        return render_template("login.html", message=message)
    
@app.route("/create_account_redirect")
def create_account_redirect():
    return render_template("create_account.html")

@app.route("/create_account")
def create_account():
    return None

@app.route("/recover_account")
def recover_account():
    return None

@app.route("/home")
def home():
    if "logged_in" in session:
        return render_template("index.html", name = "Josh!")
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT"), 5000)
    app.run(host="localhost", port=port, debug=True)
