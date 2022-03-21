from pydantic import BaseModel

from src.core.enums.phone_types import PhoneType


class Phone(BaseModel):
    type: PhoneType
    number: str
