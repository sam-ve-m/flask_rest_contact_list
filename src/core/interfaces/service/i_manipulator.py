from abc import ABC, abstractmethod
from typing import Any


class ManipulatorServiceInterface(ABC):
    @abstractmethod
    def list(self) -> dict:
        pass

    @abstractmethod
    def update(self, identifier: str, item: Any) -> dict:
        pass

    @abstractmethod
    def count(self) -> dict:
        pass
