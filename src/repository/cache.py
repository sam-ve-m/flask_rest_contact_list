import orjson

from src.repository.base.redis import RedisKeyDBRepository
from src.utils.env_config import config


class CacheRepository(RedisKeyDBRepository):
    soft_delete_folder_key = config("REDISKEYDB_FOLDER_SOFT_DELETE")
    soft_cache_key = config("REDISKEYDB_FOLDER_CACHE")

    def _add_soft_delete_folder(self, key: str) -> str:
        return f"{self.soft_delete_folder_key}:{key}"

    def _add_cache_folder(self, key: str) -> str:
        return f"{self.soft_cache_key}:{key}"

    def register_deleted_contact(self, contact_id: str) -> bool:
        return super().insert_one(self._add_soft_delete_folder(contact_id), 1)

    def check_for_deletion_history(self, contact_id: str) -> bool:
        return super().exists(self._add_soft_delete_folder(contact_id))

    def clean_deletion_history(self, contact_id: str) -> bool:
        return super().delete_one(self._add_soft_delete_folder(contact_id))

    def generate_cache_for_contact(self, contact_id: str, contact: dict) -> bool:
        contact_string = orjson.dumps(contact)
        return super().insert_one(
            self._add_cache_folder(contact_id),
            contact_string,
            300,
        )

    def get_cache_for_contact(self, contact_id: str) -> dict:
        contact_string = super().find_one(self._add_cache_folder(contact_id))
        return contact_string if contact_string is None else orjson.loads(contact_string)
