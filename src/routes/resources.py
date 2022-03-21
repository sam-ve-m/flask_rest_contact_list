from flask_restful import Resource
from src.core.entities.contact import Contact
from src.infrastructure.mongo import MongoDBInfrastructure
from src.infrastructure.redis import RedisKeyDBInfrastructure

from src.routes.adapters.reqparser_to_basemodel import JsonBodyRequestParser
from src.services.contact import ContactsService
from src.services.soft_delete import SoftDelete


class ContactRegisterResource(Resource):
    def post(self):
        contact = JsonBodyRequestParser(Contact).parse_args()
        mongo_infrastructure = MongoDBInfrastructure.get_singleton_connection()
        redis_infrastructure = RedisKeyDBInfrastructure.get_singleton_connection()
        service = SoftDelete(mongo_infrastructure, redis_infrastructure)
        return service.register(contact)


class ContactGetOneResource(Resource):
    def get(self, contact_id: str):
        infrastructure = MongoDBInfrastructure.get_singleton_connection()
        service = ContactsService(infrastructure)
        return service.get(contact_id)


class ContactGetAllResource(Resource):
    def get(self):
        infrastructure = MongoDBInfrastructure.get_singleton_connection()
        service = ContactsService(infrastructure)
        return service.list({})


class ContactGetAllByLetterResource(Resource):
    def get(self, initial_letter: str):
        infrastructure = MongoDBInfrastructure.get_singleton_connection()
        service = ContactsService(infrastructure)
        regex = f"^{initial_letter.upper()}|^{initial_letter.lower()}"
        return service.list({"firstName": {"$regex": regex}})


class ContactUpdateResource(Resource):
    def put(self, contact_id: str):
        contact = JsonBodyRequestParser(Contact, False).parse_args()
        infrastructure = MongoDBInfrastructure.get_singleton_connection()
        service = ContactsService(infrastructure)
        return service.update(contact_id, contact)


class ContactSoftDeleteResource(Resource):
    def delete(self, contact_id: str):
        mongo_infrastructure = MongoDBInfrastructure.get_singleton_connection()
        redis_infrastructure = RedisKeyDBInfrastructure.get_singleton_connection()
        service = SoftDelete(mongo_infrastructure, redis_infrastructure)
        return service.delete(contact_id)
