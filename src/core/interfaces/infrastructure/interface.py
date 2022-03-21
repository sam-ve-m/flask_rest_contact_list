from abc import ABC, abstractmethod
from typing import Any, Optional


class InfrastructureInterface(ABC):
    connection: Optional[Any]

    @classmethod
    @abstractmethod
    def get_singleton_connection(cls) -> Any:
        pass
