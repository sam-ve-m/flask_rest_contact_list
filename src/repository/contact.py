from typing import Iterator, List

from src.core.enums.status import ContactStatus
from src.repository.base.mongo import MongoDBRepository
from src.utils.env_config import config


class ContactRepository(MongoDBRepository):
    database: str = config("MONGODB_DATABASE_CONTACT")
    collection: str = config("MONGODB_COLLECTION_REGISTERS")

    def insert_contact(self, contact: dict) -> bool:
        contact.update(ContactStatus.AVAILABLE.value)
        return self.insert_one(contact)

    def find_contact(self, contact_id: str) -> dict:
        return self.find_one(
            contact_id,
            ContactStatus.AVAILABLE.value,
            projection={"active": 0},
        )

    def list_contacts(self, filter_query: dict) -> List[dict]:
        filter_query.update(ContactStatus.AVAILABLE.value)
        contacts_list = [
            contact for contact in self.find_all(
                filter_query, projection={"active": 0}
            )
        ]
        return contacts_list

