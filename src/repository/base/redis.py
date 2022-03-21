from typing import Any

from redis.client import Redis

from src.core.interfaces.repository.i_redis import RedisRepositoryInterface


class KeyDBRepository(RedisRepositoryInterface):
    def __init__(self, infrastructure: Redis):
        self.connection = infrastructure

    def insert_one(self, key: str, value: Any) -> bool:
        return self.connection.set(key, value)

    def delete_one(self, key: str) -> bool:
        deleted_items_count = self.connection.delete(key)
        return deleted_items_count > 0

    def exists(self, key: str) -> bool:
        items_count = self.connection.exists(key)
        return items_count > 0

    def find_one(self, key: str) -> dict:
        item = self.connection.get(key)
        return item
