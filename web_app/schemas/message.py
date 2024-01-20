from pydantic import BaseModel
from web_app.schemas.phone import Phone


class Message(BaseModel):
    message_text: str
    from_phone: Phone
    username: str
