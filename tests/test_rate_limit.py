import json
import pytest
from random import randint

from app.db.db import IPersistentStorage
from app.limit_rater import RateLimiter

RATE_LIMIT = 5
REFILL_RATE = 30


def generate_random_ip():
    return ".".join(str(randint(0, 255)) for _ in range(4))


@pytest.fixture
def redis_client():
    import fakeredis

    return fakeredis.FakeStrictRedis(version=6)


@pytest.fixture
def get_peristent_storage(redis_client):
    class PersistentStorage(IPersistentStorage):
        def __init__(self, client):
            self.db = client

        def get_token(self, key: str):
            return self.db.get(key)

        def add_token(self, key: str, value: str, ttl: int):
            return self.db.set(key, value, ex=ttl)

    return PersistentStorage(redis_client)


def test_ip_has_no_record_in_db(redis_client, get_peristent_storage):
    random_ip = generate_random_ip()
    capacity = 10
    persistant_storage = get_peristent_storage
    limit_rater = RateLimiter(
        capacity=capacity, refill_interval=REFILL_RATE, db=persistant_storage
    )

    result = limit_rater.consume(random_ip)
    exist_a_record = redis_client.get(random_ip)

    assert result == True
    assert exist_a_record != None


def test_ip_token_subtraction(redis_client, get_peristent_storage):
    random_ip = generate_random_ip()
    capacity = 10
    number_of_request = 5
    persistant_storage = get_peristent_storage
    limit_rater = RateLimiter(
        capacity=capacity, refill_interval=REFILL_RATE, db=persistant_storage
    )

    for _ in range(number_of_request):
        limit_rater.consume(random_ip)

    record = redis_client.get(random_ip)
    tokens = json.loads(record.decode("utf-8").replace("'", '"'))["token"]

    assert tokens == 5


def test_ip_reach_limit(redis_client, get_peristent_storage):
    random_ip = generate_random_ip()
    capacity = 10
    number_of_request = 20
    persistant_storage = get_peristent_storage
    limit_rater = RateLimiter(
        capacity=capacity, refill_interval=REFILL_RATE, db=persistant_storage
    )

    result = None
    for _ in range(number_of_request):
        result = limit_rater.consume(random_ip)

    record = redis_client.get(random_ip)
    tokens = json.loads(record.decode("utf-8").replace("'", '"'))["token"]

    assert tokens == 0
    assert result == False
