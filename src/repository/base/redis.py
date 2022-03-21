from typing import Any

from redis.client import Redis

from src.core.interfaces.repository.i_redis import RedisRepositoryInterface


class RedisKeyDBRepository(RedisRepositoryInterface):
    def __init__(self, infrastructure: Redis):
        self.redis_connection = infrastructure

    def insert_one(self, key: str, value: Any) -> bool:
        return self.redis_connection.set(key, value)

    def delete_one(self, key: str) -> bool:
        deleted_items_count = self.redis_connection.delete(key)
        return deleted_items_count > 0

    def exists(self, key: str) -> bool:
        items_count = self.redis_connection.exists(key)
        return items_count > 0

    def find_one(self, key: str) -> dict:
        item = self.redis_connection.get(key)
        return item
