import asyncio
import os
import platform
from telethon import TelegramClient, events
from dotenv import load_dotenv

from web_app.qr import QR

from wildberries.wildberries import main

load_dotenv()


@events.register(event=events.NewMessage(pattern="(wild:)(.*)"))
async def parser_handler(event):
    texts = await main(event.raw_text[5:])
    for text in texts:
        await event.respond(text)


class TgClient:
    def __init__(self, name: str):
        self.client = TelegramClient(name, api_id=int(os.getenv("API_ID")), api_hash=os.getenv("API_HASH"),
                                     device_model=platform.machine(), system_version=platform.system())
        """Если необходимо использовать на тест сервере то ставим в env значение True"""
        if os.getenv("TEST") == "True":
            self.client.session.set_dc(1, '149.154.167.40', 80)

        self.client.add_event_handler(parser_handler)

    async def start(self):
        await self.client.start()
        await self.connect()

    async def run(self):
        await self.client.run_until_disconnected()

    async def check_login(self):
        return await self.client.is_user_authorized()

    async def connect(self):
        try:
            if not self.client.is_connected():
                await self.client.connect()
        except Exception as e:
            print(e)

    async def qr_code_func(self):
        await self.connect()
        self.qr_code = await self.client.qr_login()
        QR(self.qr_code.url).save()

    async def wait(self):
        try:
            await self.qr_code.wait()
        except asyncio.exceptions.TimeoutError:
            print("Timeout on qr code")

    async def send_message(self, text: str, uname: str):
        await self.client.send_message(entity=uname, message=text)

    async def get_messages(self, uname: str):
        data = await self.client.get_messages(entity=uname, limit=10)
        resp = []
        is_self = False
        for d in data:
            if uname == "me":
                is_self = True
            resp.append({"username": str(uname), "is_self": is_self, "text": str(d.message)})
        return resp


async def listener():
    a = TgClient("test")
    await a.qr_code_func()
    await a.wait()
    await a.run()


if __name__ == '__main__':
    asyncio.run(listener())
