from typing import List, Optional

from pydantic import BaseModel, validator

from src.core.entities.phone import Phone


class Contact(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    address: Optional[str]
    phoneList: Optional[List[Phone]]

    @validator('phoneList', always=True)
    def max_of_three_phones(cls, phone_list: list, values):
        if not isinstance(phone_list, list):
            return phone_list
        phones_amount = len(phone_list)
        if phones_amount > 3:
            raise ValueError(f"Phones must be less than 3. Given {phones_amount} phones")
        cls._create_id_field(values)
        return phone_list

    @staticmethod
    def _create_id_field(values):
        id_hash = (
            values.get("firstName")
            + values.get("lastName")
            + values.get("email")
        )
        values.update({"_id": id_hash})
