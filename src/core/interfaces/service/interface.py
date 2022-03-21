from abc import ABC, abstractmethod
from typing import Any


class ServiceInterface(ABC):
    @abstractmethod
    def register(self, item: Any) -> dict:
        pass

    @abstractmethod
    def get(self, identifier: str) -> dict:
        pass

    @abstractmethod
    def list(self, filter_query: dict) -> dict:
        pass

    @abstractmethod
    def update(self, identifier: str, item: Any) -> dict:
        pass
