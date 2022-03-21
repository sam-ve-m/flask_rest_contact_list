from abc import ABC, abstractmethod
from typing import Any


class RedisRepositoryInterface(ABC):
    @abstractmethod
    def insert_one(self, key: str, value: Any, ttl_in_seconds: int = None) -> bool:
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
