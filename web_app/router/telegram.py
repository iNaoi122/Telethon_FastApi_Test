from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse


from web_app.schemas.message import Message
from web_app.schemas.phone import Phone

tg = APIRouter()


@tg.post("/login", tags=["auth"])
async def login(request: Request, phone: str):

    return request.url_for("image")


@tg.get("/check/login", tags=["auth"])
async def check_login(phone: str):
    return JSONResponse(status_code=200, content={"status": 'waiting_qr_login'})


@tg.get("/messages", tags=["message"])
async def get_messages(phone: str, uname: str):
    return JSONResponse(status_code=200, content={"messages": []})


@tg.post("/messages", tags=["message"])
async def send_messages(message: Message):
    return JSONResponse(status_code=200, content={"status": "ok"})


@tg.get("/image", tags=["auth"])
async def image(request: Request):
    return FileResponse("static/qr.png", media_type="image/png")
