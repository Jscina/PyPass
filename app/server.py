from secrets import token_hex
from backend import create_account, login, recover_account, index
from fastapi import FastAPI
import uvicorn
from fastapi.templating import Jinja2Templates
from dataclasses import dataclass, field
from threading import Thread, Event


@dataclass
class Server:
    """Server class for the PyPass application"""
    _server: FastAPI
    _templates: Jinja2Templates
    _debug: bool = field(default=False)
    _server_thread: Thread = field(init=False)
    _event_loop: Event = field(init=False)

    def __post_init__(self) -> None:
        self._server_thread = Thread(target=self.start_server)
        self._kill_thread = Event()

    @property
    def server(self) -> FastAPI:
        return self._server

    @property
    def debug(self) -> bool:
        return self._debug

    @property
    def server_thread(self) -> Thread:
        return self._server_thread

    def __enter__(self):
        # Configure the server
        self._config_server()
        # Register the views
        self._register_views()
        # Start the server process
        self.server_thread.start()

    def __exit__(self, exc_type, exc_value, traceback):
        # Stop the server process
        self.server_thread.join()

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
        """Starts the Uvicorn server

        Note: This can be used standalone for development purposes

        Args:
            debug (bool, optional): Set to True to enable debug mode. Defaults to False.
        """
        uvicorn.run(app="app:app", host="0.0.0.0", port=5000)


def main(**server_args: dict[str, str]) -> None:
    from fastapi.templating import Jinja2Templates
    from fastapi.staticfiles import StaticFiles
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates(directory="templates")

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
