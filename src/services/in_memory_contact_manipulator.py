import orjson

from src.core.entities.contact import Contact
from src.core.interfaces.service.i_soft_delete import SoftDeleteServiceInterface
from src.repository.cache import CacheRepository
from src.repository.contact import ContactRepository
from src.services.utils.status import label_status


class InMemoryContactManipulator(SoftDeleteServiceInterface):
    def __init__(self, cache_repository: CacheRepository, contact_repository: ContactRepository):
        self.contact_repository = contact_repository
        self.cache_repository = cache_repository
        self.register_methods_by_deletion_history = {
            False: lambda x: contact_repository.insert_contact(x),
            True: lambda x: all((
                contact_repository.recover_contact(x),
                cache_repository.clean_deletion_history(x.get("_id")),
            ))
        }

    def delete(self, contact_id: str) -> dict:
        mongo_delete_status = self.contact_repository.soft_delete_contact(contact_id)
        redis_register_status = self.cache_repository.register_deleted_contact(contact_id)
        return label_status(mongo_delete_status and redis_register_status)

    def register(self, contact: Contact) -> dict:
        contact_as_json = contact.json()
        contact_as_dict = orjson.loads(contact_as_json)
        contact_id = contact_as_dict.get("_id")
        has_deletions_history = self.cache_repository.check_for_deletion_history(contact_id)
        register_method = self.register_methods_by_deletion_history.get(has_deletions_history)
        register_status = register_method(contact_as_dict)
        return label_status(register_status)

    def get(self, contact_id: str) -> dict:
        if not (contact := self.cache_repository.get_cache_for_contact(contact_id)):
            if not (contact := self.contact_repository.find_contact(contact_id)):
                return label_status(False)
        cache_status = self.cache_repository.generate_cache_for_contact(contact_id, contact)
        contact.update(label_status(cache_status))
        contact.update({"contactId": contact_id})
        del contact["_id"]
        return contact
