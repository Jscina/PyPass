# Main Entry Point for the application
import webview
from flask import Flask
from server import Server

server_args = {
    "import_name": __name__,
    "static_url_path": "",
    "static_folder": "static",
    "template_folder": "templates"
}

app = Flask(**server_args)

if __name__ == "__main__":
    server_url = "http://localhost:5000"
    with Server(app):
        window = webview.create_window(
            title="PyPass",
            url=server_url
        )
        webview.start()
