# Main Entry Point for the application
from contextlib import redirect_stdout
from io import StringIO

import webview
from server import Server



if __name__ == "__main__":
    stream = StringIO()
    server_url = "http://localhost:5000"
    with redirect_stdout(stream), Server():
        window = webview.create_window(
            title="PyPass",
            url=server_url
        )
        webview.start()
        
            