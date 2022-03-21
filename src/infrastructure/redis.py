from redis import Redis

from src.infrastructure.base.singleton_connection import SingletonInfrastructure
from src.utils.env_config import config


class RedisKeyDBInfrastructure(SingletonInfrastructure):
    @staticmethod
    def _get_connection() -> Redis:
        host = config("REDISKEYDB_HOST")
        port = int(config("REDISKEYDB_PORT"))
        password = config("REDISKEYDB_PASSWORD")
        database = int(config("REDISKEYDB_DATABASE"))
        connection = Redis(host=host, port=port, password=password, db=database)
        return connection
