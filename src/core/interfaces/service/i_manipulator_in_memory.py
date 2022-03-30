from abc import ABC, abstractmethod
from typing import Any


class InMemoryServicesInterface(ABC):
    @abstractmethod
    def get(self, identifier: str) -> dict:
        pass

    @abstractmethod
    def delete(self, identifier: str) -> dict:
        pass

    @abstractmethod
    def register(self, item: Any) -> dict:
        pass
