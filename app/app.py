# Main Entry Point for the application
import webview
from flask import Flask
from server import Server

def main(app:Flask, server_url:str = "http://localhost:5000"):
    """Main entry point for the application

    Args:
        app (Flask): Flask application instance
        server_url (str, optional): The URL for the Flask server. Defaults to "http://localhost:5000".
    """
    with Server(app, False):
        webview.create_window(
            title="PyPass",
            url=server_url
        )
        webview.start()

if __name__ == "__main__":
        
    server_args = {
        "import_name": __name__,
        "static_url_path": "",
        "static_folder": "static",
        "template_folder": "templates"
    }

    app = Flask(**server_args)
    main(app=app)