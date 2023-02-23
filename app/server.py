from multiprocessing import Process
from secrets import token_hex

from backend.create_account import create_account_view
from backend.index import index_view
from backend.login import login_view
from backend.recover_account import recover_account_view
from flask import Flask, render_template


class Server:
    def __init__(self,
                 import_name: str = __name__,
                 static_url_path: str = "",
                 static_folder: str = "static",
                 template_folder: str = "templates") -> None:
        # Setup up the Flask server
        __server_args = {
            "import_name": import_name,
            "static_url_path": static_url_path,
            "static_folder": static_folder,
            "template_folder": template_folder
        }
        self.__server = Flask(**__server_args)
        self.__server_process = Process(target=self.start_server)

    @property
    def server(self) -> Flask:
        return self.__server

    @property
    def server_process(self) -> Process | None:
        return self.__server_process

    @server_process.setter
    def server_process(self, new_server: Process) -> None:
        self.__server_process = new_server       
        
    def __enter__(self):
        # Configure the server
        self._config_server()
        # Register the views
        self._register_views()
        # Start the server process
        self.server_process.start()

    def __exit__(self, exc_type, exc_value, traceback):
        # Stop the server process
        self.server_process.terminate()
        self.server_process.join()

    def _config_server(self) -> None:
        # Basic config for the server
        self.server.secret_key = token_hex(16)
        self.server.config["SESSION_COOKIE_SAMESITE"] = "Lax"
        self.server.config["SESSION_COOKIE_SECURE"] = True
        self.server.config["SESSION_COOKIE_HTTPONLY"] = True

    def _register_views(self) -> None:
        # Group views into a tuple
        views = (
            index_view,
            create_account_view,
            login_view,
            recover_account_view
        )
        # Register the views with the server
        for view in views:
            self.server.register_blueprint(view)
    
    def start_server(self) -> None:
        """Starts the Flask server

        Note: This can be used standalone for development purposes

        Args:
            debug (bool, optional): Set to True to enable debug mode. Defaults to False.
        """
        self.server.run(host="localhost", port=5000, debug=True)
        
if __name__ == "__main__":
    with Server():
        while True:
            pass
