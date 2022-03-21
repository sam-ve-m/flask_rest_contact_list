from src.core.entities.contact import Contact
from src.core.enums.status import ResponseStatus
from src.core.interfaces.service.interface import ServiceInterface
from src.repository.contact import ContactRepository
import orjson


class ContactsService(ContactRepository, ServiceInterface):
    @staticmethod
    def _label_status(status: bool) -> dict:
        status_enum_schema = {
            False: ResponseStatus.ERROR,
            True: ResponseStatus.SUCCESS,
        }
        status_enum = status_enum_schema.get(status)
        return {"status": status_enum.value}

    def register(self, contact: Contact) -> dict:
        contact_as_json = contact.json()
        contact_as_dict = orjson.loads(contact_as_json)
        register_status = self.insert_contact(contact_as_dict)
        return self._label_status(register_status)

    def get(self, contact_id: str) -> dict:
        contact_object = self.find_contact(contact_id)
        contact_id = contact_object.pop("_id")
        contact_object.update({"contactId": contact_id})
        return contact_object

    def list(self, filter_query: dict) -> dict:
        contacts_list = self.list_contacts(filter_query)
        list_status = len(contacts_list) > 0
        return {
            "contactsList": contacts_list,
            "status": self._label_status(list_status)
        }

    def update(self, contact_id: str, contact: Contact) -> dict:
        contact_as_json = contact.json()
        contact_as_dict = orjson.loads(contact_as_json)
        filtered_dict = {
            key: contact_as_dict.get(key)
            for key in filter(lambda key: contact_as_dict.get(key), contact_as_dict)
        }
        update_status = self.update_one(contact_id, filtered_dict)
        return self._label_status(update_status)
