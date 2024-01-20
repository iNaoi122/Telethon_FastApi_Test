import asyncio
from telethon import TelegramClient
from telethon import events

from web_app.qr import QR


class TgClient:
    def __init__(self, phone: str, api_id: int, api_hash: str):
        self.client = TelegramClient("me", api_id=api_id, api_hash=api_hash)
        self.phone = phone
        self.client.add_event_handler(self.parser, event=events.NewMessage())

    async def start(self):
        self.client.start()
        await self.connect()

    async def connect(self):
        if not self.client.is_connected():
            await self.client.connect()

    async def qr_code(self):
        await self.connect()
        qr_code = await self.client.qr_login()
        QR(qr_code.url).save()
        await qr_code.wait()

    @staticmethod
    async def parser(event: events.NewMessage):
        print(event.text)

    async def send_message(self, text: str, uname: str):
        await self.client.send_message(entity=uname, message=text)

    async def get_messages(self, uname: str):
        return await self.client.get_messages(entity=uname, limit=10)


async def main():
    a = TgClient()
    await a.start()
    await a.qr_code()
    print(await a.client.is_user_authorized())
    await a.send_message("some", "me")


if __name__ == '__main__':
    asyncio.run(main())
