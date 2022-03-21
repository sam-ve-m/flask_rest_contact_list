from typing import List
from pydantic import BaseModel, validator, ValidationError

from src.core.entities.phone import Phone


class Contact(BaseModel):
    firstName: str
    lastName: str
    address: str
    email: str
    phoneList: List[Phone]

    @validator('phoneList')
    def max_of_three_phones(cls, phone_list: list):
        phones_amount = len(phone_list)
        if len(phone_list) > 3:
            raise ValueError(f"Phones must be less than 3. Given {phones_amount} phones")
        return phone_list
