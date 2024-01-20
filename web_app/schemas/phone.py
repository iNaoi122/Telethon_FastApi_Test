from re import search, I
from pydantic import BaseModel, field_validator


class Phone(BaseModel):
    phone: str

    @field_validator("phone")
    def phone_validator(cls, number):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if number and not search(regex, number, I):
            raise ValueError("Phone Number Invalid.")
        return number