# Main Entry Point for the Application
import webview
from server import Server

server = Server(__name__)
testing = True

if __name__ == "__main__":

    if not testing:
        server.run_server()
        webview.create_window(title="PyPass", url="http://localhost:5000")
        webview.start()
    server.run_testing_sever()
