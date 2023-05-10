import webview
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import server as srv


def main(
    app: FastAPI,
    static_files: StaticFiles,
    templates: Jinja2Templates,
    host: str = "127.0.0.1",
    port: int = 8000,
) -> None:
    with srv.Server(
        server=app, static_files=static_files, templates=templates, host=host, port=port
    ) as server:
        server.start_server()
        webview.create_window(title="PyPass", url=f"http://{host}:{port}")
        # This is a blocking call when the user closes the window the program will exit
        match srv.OPERATING_SYSTEM:
            case srv.OS.LINUX | srv.OS.MACOS:
                webview.start(gui="gtk")
            case srv.OS.WINDOWS:
                webview.start(gui="cef")
            case _:
                raise srv.UnknownOSError()


if __name__ == "__main__":
    app = FastAPI()
    static_files = StaticFiles(directory="app/static")
    templates = Jinja2Templates(directory="app/templates")
    main(app=app, static_files=static_files, templates=templates)
