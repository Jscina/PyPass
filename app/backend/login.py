from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import Database, get_database
from schemas import LoginData

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.post('/login')
async def login(login_data: LoginData, request: Request, db: Database = Depends(get_database)) -> Response:
    try:
        login = await db.login(**login_data.dict())
    except ValueError as e:
        return JSONResponse({"status": "error", "message": f"{e}"})

    if isinstance(login, bool) and not login:
        return JSONResponse({"status": "error", "message": "Invalid username or password"})

    assert isinstance(login, tuple), f"Expected tuple, got {type(login)}"
    logged_in, user = login

    if logged_in:
        request.session["logged_in"] = True
        response = JSONResponse({"status": "success"})
        response.set_cookie("user_id", str(user.id),
                            secure=False, samesite="Strict", httponly=True)
        response.set_cookie("logged_in", "True", secure=False,
                            samesite="Strict", httponly=True)
        return response

    message = "Invalid username or password"
    return JSONResponse({"status": "error", "message": message}, status_code=401)


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("logged_in", None)
    return RedirectResponse("/")
