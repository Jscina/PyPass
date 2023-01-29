import secrets
from dataclasses import dataclass

from authentication import Auth
from database import Database
from flask import Flask, redirect, render_template, request, session
from threading import Thread
from typing import Self


@dataclass
class Server:
    name: str

    def __post_init__(self):
        self.app = Flask(self.name, static_url_path="",
                         static_folder="static", template_folder="templates")
        self.app.secret_key = secrets.token_hex(16)
        for endpoint in self.endpoints:
            self.add_endpoint(**endpoint)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name,
                              handler, methods=methods, *args, **kwargs)

    @property
    def endpoints(self) -> list[dict]:
        return self.__get_endpoints()

    def __get_endpoints(self) -> list[dict]:
        endpoints = [
            {
                'endpoint': '/',
                'endpoint_name': 'index',
                'handler': self.index,
                'methods': ['GET']
            },
            {
                'endpoint': '/login',
                'endpoint_name': 'login',
                'handler': self.login,
                'methods': ['POST']
            },
            {
                'endpoint': '/create_account_redirect',
                'endpoint_name': 'create_account_redirect',
                'handler': self.create_account_redirect,
                'methods': ['GET']
            },
            {
                'endpoint': '/create_account',
                'endpoint_name': 'create_account',
                'handler': self.create_account,
                'methods': ['GET']
            },
            {
                'endpoint': '/recover_account',
                'endpoint_name': 'recover_account',
                'handler': self.recover_account,
                'methods': ['GET']
            },
            {
                'endpoint': '/home',
                'endpoint_name': 'home',
                'handler': self.home,
                'methods': ['GET']
            }
        ]
        return endpoints

    def index(self):
        return render_template("login.html")

    def login(self):
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "admin":
            session["logged_in"] = True
            return redirect("/home")
        else:
            message = "Invalid username or password"
            return render_template("login.html", message=message)

    def create_account_redirect(self):
        return render_template("create_account.html")

    def create_account(self):
        return None

    def recover_account(self):
        return None

    def home(self):
        if "logged_in" in session:
            return render_template("index.html", name="Josh!")
        return redirect("/")

    def run_server(self,  host: str = "localhost", port: int = 5000, debug: bool = False) -> None:
        server = Thread(target=self.app.run, args=((host, port, debug)))
        server.setDaemon(True)
        server.start()
