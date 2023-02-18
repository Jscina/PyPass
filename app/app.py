# Main Entry Point for the serverlication
from threading import Thread

import webview
from contextlib import redirect_stdout
from io import StringIO
from server import server


def run_server(host: str = "localhost",
               port: int = 5000,
               debug: bool = False) -> None:
    Thread(target=server.run, args=((host, port, debug)), daemon=True).start()


if __name__ == "__main__":
    stream = StringIO()
    with redirect_stdout(stream):
        window = webview.create_window("PyPass", server)
        webview.start(debug=True)
