from abc import ABC
from typing import Iterator

from pymongo import MongoClient, errors

from src.core.interfaces.repository.i_mongo import MongoRepositoryInterface
from src.infrastructure.mongo import MongoDBInfrastructure


class MongoDBRepository(MongoRepositoryInterface, ABC):
    database: str
    collection: str

    def __init__(self):
        infrastructure: MongoClient = MongoDBInfrastructure.get_singleton_connection()
        database = infrastructure[self.database]
        self.mongo_connection = database[self.collection]

    def insert_one(self, value: dict) -> bool:
        try:
            self.mongo_connection.insert_one(value, )
            return True
        except errors.DuplicateKeyError:
            return False

    def update_one(self, identifier: str, value: dict) -> bool:
        updates = self.mongo_connection.update_one(
            {"_id": identifier},
            {"$set": value}
        )
        return updates.modified_count > 0

    def find_one(self, identifier: str, filter_query: dict, projection: dict) -> dict:
        value = self.mongo_connection.find_one({"_id": identifier, **filter_query})
        return value

    def find_all(self, query: dict, projection: dict) -> Iterator[dict]:
        values = self.mongo_connection.find(query, projection=projection)
        return values

    def aggregate(self, pipeline: list) -> Iterator[dict]:
        values = self.mongo_connection.aggregate(pipeline)
        return values
