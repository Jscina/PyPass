# Main Entry Point for the application
from fastapi import FastAPI
from backend import login, create_account, index, recover_account
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.sessions import SessionMiddleware
from secrets import token_urlsafe

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_middleware(ServerErrorMiddleware, debug=True)
app.add_middleware(SessionMiddleware, secret_key=token_urlsafe(16))
templates = Jinja2Templates(directory="app/templates")
routers = (login.router, create_account.router,
           index.router, recover_account.router)

for router in routers:
    app.include_router(router)


uvicorn.run(app, host="127.0.0.1", port=8000)
