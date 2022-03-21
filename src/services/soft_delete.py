import orjson

from src.core.entities.contact import Contact
from src.core.interfaces.service.i_soft_delete import SoftDeleteServiceInterface
from src.repository.cache import CacheRepository
from src.repository.contact import ContactRepository
from src.services.utils.status import label_status


class SoftDelete(CacheRepository, ContactRepository, SoftDeleteServiceInterface):
    def __init__(self, mongo_infrastructure, redis_infrastructure):
        super(CacheRepository, self).__init__(redis_infrastructure)
        super(ContactRepository, self).__init__(mongo_infrastructure)
        self.register_methods_by_deletion_history = {
            False: lambda x: self.insert_contact(x),
            True: lambda x: all((
                self.recover_contact(x.get("_id")),
                self.clean_deletion_history(x.get("_id")),
            ))
        }

    def delete(self, contact_id: str) -> dict:
        mongo_delete_status = self.delete_contact(contact_id)
        redis_register_status = self.register_deleted_contact(contact_id)
        return label_status(mongo_delete_status and redis_register_status)

    def register(self, contact: Contact) -> dict:
        contact_as_json = contact.json()
        contact_as_dict = orjson.loads(contact_as_json)
        contact_id = contact_as_dict.get("_id")
        has_deletions_history = self.check_for_deletion_history(contact_id)
        register_method = self.register_methods_by_deletion_history.get(has_deletions_history)
        register_status = register_method(contact_as_dict)
        return label_status(register_status)

    def get(self, contact_id: str) -> dict:
        contact = self.get_cache_for_contact(contact_id)
        if contact is None:
            contact = self.find_contact(contact_id)
        if contact is None:
            return label_status(False)
        cache_status = self.generate_cache_for_contact(contact_id, contact)
        contact.update(label_status(cache_status))
        contact.update({"contactId": contact_id})
        del contact["_id"]
        return contact
