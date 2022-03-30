import orjson

from src.core.entities.contact import Contact
from src.core.interfaces.service.i_manipulator_in_memory import InMemoryServicesInterface
from src.repository.cache import CacheRepository
from src.repository.contact import ContactRepository
from src.services.utils.status import label_status


class InMemoryContactManipulator(InMemoryServicesInterface):
    def __init__(self, redis_cache_repository: CacheRepository, mongo_contact_repository: ContactRepository):
        self.mongo_contact_repository = mongo_contact_repository
        self.redis_cache_repository = redis_cache_repository
        self.register_methods_by_deletion_history = {
            False: mongo_contact_repository.insert_contact,
            True: self.recover_contact
        }

    def delete(self, contact_id: str) -> dict:
        mongo_delete_status = self.mongo_contact_repository.soft_delete_contact(contact_id)
        redis_register_status = self.redis_cache_repository.set_inactive_contact(contact_id)
        return label_status(mongo_delete_status and redis_register_status)

    def register(self, contact: Contact) -> dict:
        contact_as_json = contact.json()
        contact_as_dict = orjson.loads(contact_as_json)
        contact_id = contact_as_dict.get("_id")
        is_contact_active = self.redis_cache_repository.is_contact_inactive(contact_id)
        register_method = self.register_methods_by_deletion_history.get(is_contact_active)
        register_status = register_method(contact_as_dict)
        return label_status(register_status)

    def get(self, contact_id: str) -> dict:
        if not (contact := self.redis_cache_repository.get_contact_cache(contact_id)):
            if not (contact := self.mongo_contact_repository.find_contact(contact_id)):
                return label_status(False)
        cache_status = self.redis_cache_repository.set_contact_cache(contact_id, contact)
        contact.update(label_status(cache_status))
        contact.update({"contactId": contact_id})
        del contact["_id"]
        return contact

    def recover_contact(self, contact: dict) -> bool:
        recover_status = self.mongo_contact_repository.recover_contact(contact),
        clean_status = self.redis_cache_repository.delete_contact_inactive_register(contact.get("_id")),
        register_status = all((recover_status, clean_status))
        return register_status
