from abc import ABC
from typing import Iterator

from pymongo import MongoClient, errors

from src.core.interfaces.repository.i_mongo import MongoRepositoryInterface


class MongoDBRepository(MongoRepositoryInterface, ABC):
    database: str
    collection: str

    def __init__(self, infrastructure: MongoClient):
        database = infrastructure[self.database]
        self.connection = database[self.collection]

    def insert_one(self, value: dict) -> bool:
        try:
            self.connection.insert_one(value)
            return True
        except errors.DuplicateKeyError:
            return False

    def update_one(self, identifier: str, value: dict) -> bool:
        updates = self.connection.update_one(identifier, {"$set": value})
        return updates.modified_count > 0

    def find_one(self, identifier: str) -> dict:
        value = self.connection.find_one({"_id": identifier})
        return value

    def find_all(self, query: dict = {}, projection: dict = {}) -> Iterator[dict]:
        values = self.connection.find(query, projection=projection)
        return values