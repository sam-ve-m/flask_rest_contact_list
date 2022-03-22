from typing import List

from src.core.enums.status import ContactStatus
from src.repository.base.mongo import MongoDBRepository
from src.utils.env_config import config


class ContactRepository(MongoDBRepository):
    database: str = config("MONGODB_DATABASE_CONTACT")
    collection: str = config("MONGODB_COLLECTION_REGISTERS")

    count_phones_pipeline = [
        {'$match': ContactStatus.AVAILABLE.value},
        {'$project': {
            '_id': 0,
            'phoneList': 1
        }},
        {'$unwind': '$phoneList'},
        {'$group': {
            '_id': '$phoneList.type',
            'Count': {'$count': {}}
        }}
    ]

    def insert_contact(self, contact: dict) -> bool:
        contact.update(ContactStatus.AVAILABLE.value)
        return super().insert_one(contact)

    def find_contact(self, contact_id: str) -> dict:
        return super().find_one(
            contact_id,
            ContactStatus.AVAILABLE.value,
            projection={"active": 0},
        )

    def list_contacts(self, filter_query: dict) -> List[dict]:
        filter_query.update(ContactStatus.AVAILABLE.value)
        contacts_list = []
        for contact in super().find_all(filter_query, projection={"active": 0, "address": 0}):
            contact_id = contact.pop("_id")
            contact.update({"contactId": contact_id})
            contacts_list.append(contact)
        return contacts_list

    def update_contact(self, contact_id: str, filtered_dict: dict) -> bool:
        filtered_dict.update(ContactStatus.AVAILABLE.value)
        return super().update_one(contact_id, filtered_dict)

    def delete_contact(self, contact_id: str) -> bool:
        return super().update_one(contact_id, ContactStatus.UNAVAILABLE.value)

    def recover_contact(self, contact: dict) -> bool:
        contact_id = contact.get("_id")
        phone_list = contact.pop("phoneList")
        phone_list = {f"phoneList.{index}": phone for index, phone in enumerate(phone_list)}
        contact.update(**ContactStatus.AVAILABLE.value, **phone_list)
        return super().update_one(contact_id, contact)

    def count_phones_types(self) -> list:
        phones_count = [phone_type for phone_type in super().aggregate(self.count_phones_pipeline)]
        return phones_count
