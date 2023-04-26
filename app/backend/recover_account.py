import logging
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from database import Database, get_database, close_database

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get('/recover_account', response_class=HTMLResponse)
async def recover_account(request: Request):
    return templates.TemplateResponse("recover_account.html", {"request": request})

@router.post("/recover")
async def recover(email: str, password: str, confirm_password: str, db: Database = Depends(get_database)) -> Response:
    if password != confirm_password:
        response = {
            "status": "failure",
            "message": "Passwords do not match"
        }
        return JSONResponse(response)

    accounts = db.fetch_user(email)
    
    close_database(db)
