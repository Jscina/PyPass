# Main Entry Point for the serverlication
from threading import Thread

import webview
from server import server


def run_server(host: str = "localhost", port: int = 5000, debug: bool = False) -> None:
    Thread(target=server.run,
            args=((host,port,debug)),
            daemon=True) \
    .start()

if __name__ == "__main__":
    run_server()
    webview.create_window(
        title="PyPass",
        url="http://localhost:5000"
        )
    webview.start()

