from src.repository.base.mongo import MongoDBRepository
from src.utils.env_config import config


class ContactRepository(MongoDBRepository):
    database: str = config("MONGODB_DATABASE_CONTACT")
    collection: str = config("MONGODB_COLLECTION_REGISTERS")

    def insert_contact(self, contact: dict) -> bool:
        return self.insert_one(contact)
