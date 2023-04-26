from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from database import Database, get_database, close_database
from schemas import UserData
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get('/create_account_redirect', response_class=HTMLResponse)
async def create_account_redirect(request: Request):
    return templates.TemplateResponse("create_account.html", {"request": request})

@router.post('/create_account')
async def create_account(user_info: UserData, db: Database = Depends(get_database)) -> Response:
    user_info:dict = user_info.dict()
    if user_info["password"] != user_info["confirm_password"]:
        message = "Passwords do not match"
        return JSONResponse({"status": "error", "message": message})
    
    user_info.pop("confirm_password")

    message = db.add_user(**user_info)

    if isinstance(message, str):
        return JSONResponse({"status": "error", "message": message})

    close_database(db)
    return RedirectResponse("/home")
