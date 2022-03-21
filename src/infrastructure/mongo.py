from pymongo import MongoClient

from src.infrastructure.base.singleton_connection import SingletonInfrastructure
from src.utils.env_config import config


class MongoDBInfrastructure(SingletonInfrastructure):

    @staticmethod
    def _get_connection() -> MongoClient:
        user = config("MONGODB_USER")
        host = config("MONGODB_HOST")
        port = config("MONGODB_PORT")
        password = config("MONGODB_PASSWORD")
        connection = MongoClient(f'mongodb://{user}:{password}@{host}:{port}/')
        return connection
