from typing import Any

from redis.client import Redis

from src.core.interfaces.repository.i_redis import RedisRepositoryInterface
from src.infrastructure.redis import RedisKeyDBInfrastructure


class RedisKeyDBRepository(RedisRepositoryInterface):
    def __init__(self):
        infrastructure: Redis = RedisKeyDBInfrastructure.get_singleton_connection()
        self.redis_connection = infrastructure

    def set(self, key: str, value: Any, ttl_in_seconds: int = None) -> bool:
        return self.redis_connection.set(key, value, ex=ttl_in_seconds)

    def delete(self, key: str) -> bool:
        deleted_items_count = self.redis_connection.delete(key)
        return deleted_items_count > 0

    def exists(self, key: str) -> bool:
        items_count = self.redis_connection.exists(key)
        return items_count > 0

    def get(self, key: str) -> str:
        item = self.redis_connection.get(key)
        return item
