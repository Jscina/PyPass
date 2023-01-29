# Main Entry Point for the Application
import webview, os
from contextlib import redirect_stdout, redirect_stderr
from server import Server

if __name__ == "__main__":
    with open(os.devnull, "w") as file, redirect_stdout(file), redirect_stderr(file):
        server = Server(__name__)
        server.run_server(debug=False)
        webview.create_window(title="PyPass", url="http://localhost:5000")
        webview.start()
