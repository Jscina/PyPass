from multiprocessing import Process
from secrets import token_hex

from backend import create_account, login, recover_account, index
from flask import Flask

class Server:
    """Server class for the PyPass application"""
    def __init__(self, app: Flask, debug:bool = False) -> None:
        # Setup up the Flask server and the database
        self._server = app
        self._debug = debug
        self._server_process = Process(target=self.start_server)
        
    @property
    def server(self) -> Flask:
        return self._server

    @property
    def debug(self) -> bool:
        return self._debug
    
    @property
    def server_process(self) -> Process:
        return self._server_process
    
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
        """Configures the Flask server"""
        # Basic config for the server
        self.server.secret_key = token_hex(16)
        self.server.config["SESSION_COOKIE_SAMESITE"] = "Lax"
        self.server.config["SESSION_COOKIE_SECURE"] = True
        self.server.config["SESSION_COOKIE_HTTPONLY"] = True

    def _register_views(self) -> None:
        """Registers the views with the server"""
        # Group views into a tuple
        views = (
            index.index_view,
            create_account.create_account_view,
            login.login_view,
            recover_account.recover_account_view
        )
        # Register the views with the server
        for blueprint in views:
            self.server.register_blueprint(blueprint)
        
    def start_server(self) -> None:
        """Starts the Flask server

        Note: This can be used standalone for development purposes

        Args:
            debug (bool, optional): Set to True to enable debug mode. Defaults to False.
        """
        self.server.run(host="localhost", port=5000, debug=self.debug)


def main(**server_args: dict[str, str]) -> None:
    app = Flask(**server_args)
    
    srv = Server(app, True)
    srv._config_server()
    srv._register_views()
    srv.start_server()

if __name__ == "__main__":
    server_args = {
    "import_name": __name__,
    "static_url_path": "",
    "static_folder": "static",
    "template_folder": "templates"
    }
    main(**server_args)