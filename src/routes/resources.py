from flask_restful import Resource
from src.core.entities.contact import Contact
from src.infrastructure.mongo import MongoDBInfrastructure

from src.routes.adapters.reqparser_to_basemodel import JsonBodyRequestParser
from src.services.register_contact import RegisterContact


class ContactResource(Resource):
    def post(self):
        contact = JsonBodyRequestParser(Contact).parse_args()
        infrastructure = MongoDBInfrastructure.get_singleton_connection()
        service = RegisterContact(infrastructure)
        return service.register_contact(contact)
