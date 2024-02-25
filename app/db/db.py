from redis import Redis, StrictRedis
from .idb import IPersistentStorage


class PersistentStorage(IPersistentStorage):
    def __init__(self, client: Redis):
        self.db = client

    def get_token(self, key: str):
        redis_client = StrictRedis(connection_pool=self.db)
        data = redis_client.get(key)
        redis_client.close()
        return data

    def add_token(self, key: str, value: str, ttl: int):
        redis_client = StrictRedis(connection_pool=self.db)
        data = redis_client.set(key, value, ex=ttl)
        redis_client.close()
        return data
