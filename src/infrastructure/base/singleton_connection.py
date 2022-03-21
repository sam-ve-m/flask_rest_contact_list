from abc import ABC, abstractmethod
from typing import Any

from src.core.interfaces.infrastructure.interface import InfrastructureInterface


class SingletonInfrastructure(InfrastructureInterface, ABC):
    connection: Any = None

    @staticmethod
    @abstractmethod
    def _get_connection() -> Any:
        pass

    @classmethod
    def get_singleton_connection(cls) -> Any:
        if cls.connection is None:
            cls.connection = cls._get_connection()
        return cls.connection
