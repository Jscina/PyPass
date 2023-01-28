from flask import Flask, redirect, render_template, request, session
import secrets

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
    
@app.route("/home")
def home():
    if "logged_in" in session:
        return render_template("index.html", name = "Josh!")
    return redirect("/")

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
