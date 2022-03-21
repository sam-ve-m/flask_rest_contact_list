from src.core.enums.status import Status
from src.repository.contact import ContactRepository


class RegisterContact(ContactRepository):
    @staticmethod
    def _label_status(status: bool) -> dict:
        status_enum_schema = {
            False: Status.ERROR,
            True: Status.SUCCESS,
        }
        status_enum = status_enum_schema.get(status)
        return {"status": status_enum.value}

    def register_contact(self, contact: dict) -> dict:
        register_status = self.insert_contact(contact)
        return self._label_status(register_status)
