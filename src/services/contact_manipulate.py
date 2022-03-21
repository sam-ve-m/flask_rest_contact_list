import orjson

from src.core.entities.contact import Contact
from src.core.interfaces.service.i_manipulator import ManipulatorServiceInterface
from src.repository.contact import ContactRepository
from src.services.utils.status import label_status


class ContactsManipulatorService(ContactRepository, ManipulatorServiceInterface):
    def list(self, filter_query: dict) -> dict:
        contacts_list = self.list_contacts(filter_query)
        list_status = len(contacts_list) > 0
        return {
            "contactsList": contacts_list,
            **label_status(list_status)
        }

    def update(self, contact_id: str, contact: Contact) -> dict:
        contact_as_json = contact.json()
        contact_as_dict = orjson.loads(contact_as_json)
        filtered_dict = {
            key: contact_as_dict.get(key)
            for key in filter(lambda key: contact_as_dict.get(key), contact_as_dict)
        }
        update_status = self.update_contact(contact_id, filtered_dict)
        return label_status(update_status)

    def count(self) -> dict:
        phones_types = self.count_phones_types()
        total_registers = sum(phone_type.get("Count") for phone_type in phones_types)
        count_status = total_registers > 0
        return {
            "countContacts": total_registers,
            "countType": phones_types,
            **label_status(count_status)
        }
