from enum import Enum


class ResponseStatus(Enum):
    SUCCESS: str = "1001"
    ERROR: str = "1004"


class ContactStatus(Enum):
    AVAILABLE: dict = {"active": True}
    UNAVAILABLE: dict = {"active": False}
