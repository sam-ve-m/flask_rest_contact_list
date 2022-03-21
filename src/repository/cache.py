from src.repository.base.redis import RedisKeyDBRepository
from src.utils.env_config import config


class CacheRepository(RedisKeyDBRepository):
    soft_delete_folder_key = config("REDISKEYDB_FOLDER_SOFT_DELETE")

    def _get_soft_delete_key(self, contact_id):
        return f"{self.soft_delete_folder_key}:{contact_id}"

    def register_deleted_contact(self, contact_id: str) -> bool:
        return super().insert_one(self._get_soft_delete_key(contact_id), 1)

    def check_for_deletion_history(self, contact_id: str) -> bool:
        return super().exists(self._get_soft_delete_key(contact_id))

    def clean_deletion_history(self, contact_id: str) -> bool:
        return super().delete_one(self._get_soft_delete_key(contact_id))
