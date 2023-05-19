import logging
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from database import Database, get_database
from collections import namedtuple

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

@router.post('/fetch_accounts')
async def fetch_accounts(request:Request, db: Database = Depends(get_database)) -> Response:
    if not db:
        logger.error("No database found in request context")
        return JSONResponse({"status": "error", "message": "Internal server error"}, status_code=500)
    logged_in = bool(request.cookies.get("logged_in"))
    user_id = int(request.cookies.get("user_id"))
    user = await db.fetch_user_by_id(logged_in, user_id)
    db.cipher.master_key = await db.fetch_master_key(user)
    try:
        accounts = await db.fetch_accounts(logged_in, user_id)
    except HTTPException as e:
        return await http_exception_handler(request, e)
    accounts = [{"service": account.service, "username": account.account_username, "password": account.account_password} for account in accounts]
    return JSONResponse(accounts)

@router.post("/add_account")
async def add_account(request: Request, account_data: dict, db: Database = Depends(get_database)) -> Response:
    if not db:
        logger.error("No database found in request context")
        return JSONResponse({"status": "error", "message": "Internal server error"}, status_code=500)
    account_data["user_id"] = int(request.cookies.get("user_id"))
    logged_in = bool(request.cookies.get("logged_in"))
    user = await db.fetch_user_by_id(logged_in, account_data["user_id"])
    db.cipher.master_key = await db.fetch_master_key(user)
    await db.add_account(account_data)
    del account_data
    return JSONResponse(content={"status": "success"})

@router.post("/delete_account")
async def delete_account(request:Request, data:dict, db: Database = Depends(get_database)) -> Response:
    user_id = int(request.cookies.get("user_id"))
    logged_in = bool(request.cookies.get("logged_in"))
    order = int(data["order"])
    try:
        await db.remove_account(logged_in, order, user_id)
    except HTTPException as e:
        return await http_exception_handler(request, e)
    return JSONResponse(content={"status":"success"})

@router.post("/get_current_user")
async def get_current_user(request: Request, db: Database = Depends(get_database)) -> Response:
    user_id = int(request.cookies.get("user_id"))
    logged_in = bool(request.cookies.get("logged_in"))
    user = await db.fetch_user_by_id(logged_in, user_id)
    return JSONResponse(content={
        "username":user.username,
        "password":bytes(user.password).decode("utf-8"),
        "email": user.email
    })

@router.post("/update_account")
async def update_account(request: Request, data:dict, db:Database = Depends(get_database)) -> Response:
    user_id = int(request.cookies.get("user_id"))
    logged_in = bool(request.cookies.get("logged_in"))
    User = namedtuple("User", ["id", "username", "email", "password"])
    data["id"] = user_id
    user = User(**data)
    if await db.update_user(logged_in, user):
        return JSONResponse(content={"status":"success"})
    else:
        return JSONResponse(content={"status":"failed"}, status_code=400)
    
      