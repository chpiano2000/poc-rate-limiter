import time
import redis
from app.limit_rater import RateLimiter
from app.db.db import PersistentStorage
from config import Config as config
from logger import logger

REFILL_RATE = 60 * 60  # 1 hour


def process(n: int, r: int, ip: str):
    """Main function
    Args:
        n (int): Number of request
        r (int): Rate limit (request/hour)
    """
    logger.info(REFILL_RATE)
    redis_client = redis.ConnectionPool.from_url(config.REDIS_SERVER)
    persistant_storage = PersistentStorage(redis_client)
    limit_rater = RateLimiter(
        capacity=r, refill_interval=REFILL_RATE, db=persistant_storage
    )
    while n > 0:
        limit_result = limit_rater.consume(ip)
        logger.info(limit_result)
        time.sleep(1)
        n -= 1


if __name__ == "__main__":
    NUMBER_OF_REQUEST = 10
    RATE_LIMIT = 5
    REFILL_RATE = 30
    process(n=NUMBER_OF_REQUEST, r=RATE_LIMIT, ip="165.192.126.20")
