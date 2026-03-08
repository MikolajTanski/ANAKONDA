import logging

from pymongo import MongoClient, UpdateOne

from config import Config

log = logging.getLogger(__name__)


class MongoStorage:
    """Zapisuje ogłoszenia do MongoDB."""

    def __init__(self, config: Config):
        self.client = MongoClient(config.MONGO_URI)
        self.collection = self.client[config.DB_NAME][config.COLLECTION_NAME]
        self.collection.create_index("id", unique=True)
        log.info("Połączono z MongoDB: %s / %s", config.DB_NAME, config.COLLECTION_NAME)

    def save(self, listings: list[dict]) -> tuple[int, int]:
        """Upsert po polu id. Zwraca (inserted, updated)."""
        if not listings:
            return 0, 0
        ops = [UpdateOne({"id": doc["id"]}, {"$set": doc}, upsert=True) for doc in listings]
        result = self.collection.bulk_write(ops, ordered=False)
        return result.upserted_count, result.modified_count
