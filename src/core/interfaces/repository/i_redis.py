from abc import ABC, abstractmethod
from typing import Any


class RedisRepositoryInterface(ABC):
    @abstractmethod
    def insert_one(self, key: str, value: Any) -> bool:
        pass

    @abstractmethod
    def delete_one(self, key: str) -> bool:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def find_one(self, key: str) -> dict:
        pass
