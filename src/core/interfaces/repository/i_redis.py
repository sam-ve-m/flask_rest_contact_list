from abc import ABC, abstractmethod
from typing import Any


class RedisRepositoryInterface(ABC):
    @abstractmethod
    def set(self, key: str, value: Any, ttl_in_seconds: int = None) -> bool:
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def get(self, key: str) -> dict:
        pass
