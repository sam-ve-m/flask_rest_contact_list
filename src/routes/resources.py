from flask_restful import Resource
from src.core.entities.contact import Contact
from src.repository.cache import CacheRepository
from src.repository.contact import ContactRepository

from src.routes.adapters.reqparser_to_basemodel import JsonBodyRequestParser
from src.services.contact_manipulator import ContactsManipulatorService
from src.services.in_memory_contact_manipulator import InMemoryContactManipulator


class ContactRegisterResource(Resource):
    def post(self):
        contact = JsonBodyRequestParser(Contact).parse_args()
        service = InMemoryContactManipulator(CacheRepository(), ContactRepository())
        return service.register(contact)


class ContactGetOneResource(Resource):
    def get(self, contact_id: str):
        service = InMemoryContactManipulator(CacheRepository(), ContactRepository())
        return service.get(contact_id)


class ContactGetAllResource(Resource):
    def get(self):
        service = ContactsManipulatorService(ContactRepository())
        return service.list()


class ContactGetAllByLetterResource(Resource):
    def get(self, initial_letter: str):
        service = ContactsManipulatorService(ContactRepository())
        return service.list_by_letter(initial_letter)


class ContactUpdateResource(Resource):
    def put(self, contact_id: str):
        contact = JsonBodyRequestParser(Contact, False).parse_args()
        service = ContactsManipulatorService(ContactRepository())
        return service.update(contact_id, contact)


class ContactSoftDeleteResource(Resource):
    def delete(self, contact_id: str):
        service = InMemoryContactManipulator(CacheRepository(), ContactRepository())
        return service.delete(contact_id)


class PhonesCountResource(Resource):
    def get(self):
        service = ContactsManipulatorService(ContactRepository())
        return service.count()
