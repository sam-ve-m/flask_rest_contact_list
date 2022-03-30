import orjson

from src.core.entities.contact import Contact
from src.core.enums.phone_types import PhoneType
from src.core.interfaces.service.i_manipulator import ManipulatorServiceInterface
from src.repository.contact import ContactRepository
from src.services.utils.status import label_status


class ContactsManipulatorService(ManipulatorServiceInterface):
    def __init__(self, repository: ContactRepository):
        self.repository = repository

    @staticmethod
    def _filter_contact_as_list_item(contact: dict):
        contact_id = contact.pop("_id")
        contact.update({"contactId": contact_id})
        del contact["address"]
        return contact

    def list(self) -> dict:
        raw_contacts_list = self.repository.list_contacts({})
        contacts_list = [
            self._filter_contact_as_list_item(raw_contact)
            for raw_contact in raw_contacts_list
        ]
        list_status = len(contacts_list) > 0
        return {
            "contactsList": contacts_list,
            **label_status(list_status)
        }

    def list_by_letter(self, initial_letter: str) -> dict:
        regex = f"^{initial_letter.upper()}|^{initial_letter.lower()}"
        filter_query = {"firstName": {"$regex": regex}}
        raw_contacts_list = self.repository.list_contacts(filter_query)
        contacts_list = [
            self._filter_contact_as_list_item(raw_contact)
            for raw_contact in raw_contacts_list
        ]
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
        update_status = self.repository.update_contact(contact_id, filtered_dict)
        return label_status(update_status)

    def count(self) -> dict:
        phones_types_counter = self.repository.count_phones_types()
        registers_ids = set()
        phones_types = set()
        for phone_type in phones_types_counter:
            contacts_ids = phone_type.pop("Contacts")
            registers_ids.update(contacts_ids)
            phones_types.add(phone_type.get("_id"))
        for missing_phone_type in set(PhoneType.__members__.keys()).difference(phones_types):
            phones_types_counter.append({
                "_id": missing_phone_type,
                "Count": 0
            })
        total_registers = len(registers_ids)
        count_status = total_registers > 0
        return {
            "countContacts": total_registers,
            "countType": phones_types_counter,
            **label_status(count_status)
        }
