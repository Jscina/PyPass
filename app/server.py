from dataclasses import dataclass, field
from secrets import token_urlsafe
from typing import Self

import uvicorn
from backend import create_account, index, login, recover_account
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.sessions import SessionMiddleware
from multiprocessing import Process

@dataclass
class Server:
    """Server class for the PyPass application"""
    server: FastAPI
    templates: Jinja2Templates
    static_files: StaticFiles
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    __server_process: Process | None = field(init=False, default=None)

    @property
    def server_process(self) -> Process:
        assert self.__server_process is not None, "No server process found"
        return self.__server_process

    def __post_init__(self) -> None:
        self.server.mount("/static", self.static_files, name="static")

    def __enter__(self) -> Self:
        self.__register_routes()
        self.__setup_middleware()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.server_process.terminate()
        self.server_process.join()

    def __register_routes(self) -> None:
        """Registers the routes with the server"""
        routers = (
            login.router,
            create_account.router,
            index.router,
            recover_account.router,
        )
        for router in routers:
            self.server.include_router(router)

    def __setup_middleware(self) -> None:
        self.server.add_middleware(ServerErrorMiddleware, debug=self.debug)
        self.server.add_middleware(SessionMiddleware, secret_key=token_urlsafe(16))

    def __start_server(self) -> None:
        """Starts the uviorn server"""
        uvicorn.run(app=self.server, host=self.host, port=self.port)
        
    def __create_server_process(self) -> Process:
        return Process(target=self.__start_server)

    def start_server(self) -> None:
        if self.__server_process is None:
            self.__server_process = self.__create_server_process()
        self.__server_process.start()

# For local testing in the browser
def main() -> None:
    app = FastAPI()
    static_files = StaticFiles(directory="app/static")
    templates = Jinja2Templates(directory="app/templates")

    with Server(app, templates, static_files) as server:
        server.start_server()
        while True:
            continue
            


if __name__ == "__main__":
    main()
