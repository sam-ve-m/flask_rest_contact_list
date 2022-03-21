from abc import ABC, abstractmethod


class MongoRepositoryInterface(ABC):
    @abstractmethod
    def insert_one(self, value: dict) -> bool:
        pass

    @abstractmethod
    def update_one(self, identifier: str, value: dict) -> bool:
        pass

    @abstractmethod
    def find_one(self, identifier: str, filter_query: dict, projection: dict) -> bool:
        pass

    @abstractmethod
    def find_all(self, query: dict, project: dict) -> bool:
        pass
