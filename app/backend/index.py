import logging
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from database import Database, get_database

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get('/index', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get('/home')
async def home(request: Request):
    logged_in = request.session.get("logged_in", False)
    if logged_in:
        return RedirectResponse('/index')
    return RedirectResponse("/")

@router.get('/fetch_accounts')
async def fetch_accounts(logged_in: bool, user_id: int, db: Database = Depends(get_database)) -> Response:
    if not db:
        logger.error("No database found in request context")
        return JSONResponse({"status": "error", "message": "Internal server error"}, status_code=500)
    accounts = await db.fetch_accounts(logged_in, user_id)
    accounts = [{account.id: {"website": account.website, "username": account.account_name, "password": account.account_password}} for account in accounts]
    return JSONResponse(accounts)

@router.post("/add_account")
async def add_account(account_data: dict, db: Database = Depends(get_database)) -> Response:
    if not db:
        logger.error("No database found in request context")
        return JSONResponse({"status": "error", "message": "Internal server error"}, status_code=500)
    website = account_data["website"]
    username = account_data["username"]
    password = account_data["password"]
    await db.add_account(website, username, password)
    del website, username, password
    return RedirectResponse("/home")
