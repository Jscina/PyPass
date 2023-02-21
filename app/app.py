# Main Entry Point for the application
from contextlib import redirect_stdout
from io import StringIO
from threading import Thread

import webview
from server import server


def run_server(host: str = "localhost",
               port: int = 5000,
               debug: bool = False) -> None:
    Thread(target=server.run, args=((host, port, debug)), daemon=True).start()


if __name__ == "__main__":
    stream = StringIO()
    with redirect_stdout(stream):
        run_server(debug=False)
        webview.create_window(
            title="PyPass",
            url="http://localhost:5000"
        )
        webview.start()
