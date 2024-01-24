import logging

from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse

from db.mongo import MongoDB
from tg_client.client import TgClient

from web_app.schemas.message import Message
from web_app.schemas.phone import Phone

logging.basicConfig(level=logging.DEBUG)

tg = APIRouter()
mongo_db = MongoDB()
tg_cli = TgClient("me")


@tg.on_event("startup")
async def start_app():
    await tg_cli.connect()
    print("Is connected TG " + str(tg_cli.client.is_connected()))
    mongo_db.check_connect()


@tg.post("/login", tags=["auth"])
async def login(request: Request, phone: str, background_tasks: BackgroundTasks):
    await tg_cli.qr_code_func()
    background_tasks.add_task(tg_cli.wait)
    return {"url": request.url_for("image")}


@tg.get("/check/login", tags=["auth"])
async def check_login(phone: str):
    try:
        is_auth: bool = await tg_cli.check_login()
        return JSONResponse(status_code=200, content={"status": is_auth})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=404, content={"status": "false"})


@tg.get("/messages", tags=["message"])
async def get_messages(phone: str, uname: str):
    try:
        messages = await tg_cli.get_messages(uname=uname)
        mongo_db.add_messages(messages)
        return JSONResponse(status_code=200, content={"messages": messages})

    except Exception as e:
        print(e)
        return JSONResponse(status_code=422, content={"Write to db Error"})


@tg.post("/messages", tags=["message"])
async def send_messages(message: Message):
    await tg_cli.send_message(message.message_text, message.username)
    return JSONResponse(status_code=200, content={"status": "ok"})


@tg.get("/image", tags=["auth"])
async def image(request: Request):
    return FileResponse("static/qr.png", media_type="image/png")
