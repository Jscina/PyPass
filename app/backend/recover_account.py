import logging
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from database import Database, get_database
from authorization import verify_values
from random import choice
import smtplib
from email.mime.text import MIMEText

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def generate_code(length:int=6) -> str:
    return "".join(choice("0123456789") for _ in range(length))

@router.get('/recover_account', response_class=HTMLResponse)
async def recover_account(request: Request):
    return templates.TemplateResponse("recover_account.html", {"request": request})

@router.post("/verify_code")
async def verify_code(request:Request, data:dict[str, str]) -> Response:
    confirm_code = request.cookies.get("confirm_code")
    if verify_values(confirm_code, data["confirm_code"]):
        return JSONResponse(content={"status":"success"})
    return JSONResponse(content={"status":"failure", "message": "Invalid code"}, status_code=400)
    
    
@router.post("/change_password")
async def change_password(data: dict[str, str], db: Database = Depends(get_database)) -> Response:
    if data["password"] != data["confirm_password"]:
        response = {
            "status": "failure",
            "message": "Passwords do not match"
        }
        return JSONResponse(response, status_code=400)
    user = await db.fetch_user(data["email"])
    user.password = data["password"]
    if await db.update_user(bool(data["verified"]), user):
        response = JSONResponse(content={"status": "success"})
        response.set_cookie(
            key="confirm_code",
            value="",
            max_age=0,
            httponly=True,
            samesite="strict"
        )
        return response
    return JSONResponse(content={"status": "failure", "message":"Failed to change password"}, status_code=400)

@router.post("/send_recovery_email")
async def send_recovery_email(data: dict[str, str], confirm_code: str = Depends(generate_code)) -> Response:
    sender = "no_reply@pypass.com"
    recipient = data["recovery_email"]
    msg = MIMEText(f'Here is the code to recover your account: {confirm_code}\n It will be valid for the next 10 minutes')
    msg['Subject'] = 'Recover PyPass Account'
    msg['From'] = sender
    msg['To'] = recipient

    try:
        smtp = smtplib.SMTP("smtp.freesmtpservers.com", port=25)
        smtp.sendmail(sender, recipient, msg.as_string())
        logger.info("Mail Sent Successfully")
    except smtplib.SMTPException as e:
        logger.error(f"Mail failed to send: {e}")
        return JSONResponse(content={"status":"failure"}, status_code=400)
    response = JSONResponse(content={"status":"success"})
    response.set_cookie(
        key="confirm_code",
        value=confirm_code,
        httponly=True,
        samesite="strict",
        max_age=600
    )
    return response
    
