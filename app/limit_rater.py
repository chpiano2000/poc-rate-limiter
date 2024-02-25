import json
import datetime
from .db.idb import IPersistentStorage


class RateLimiter:
    def __init__(
            self, 
            capacity: int, 
            refill_interval: int, 
            db: IPersistentStorage
        ):
        self.capacity = capacity
        self.refill_interval = refill_interval
        self.db = db

    def consume(self, ip: int) -> bool:
        currrent_time = datetime.datetime.now()
        data = self.db.get_token(ip)
        if not data:
            self.db.add_token(
                key=ip,
                value=str(
                    {
                        "token": self.capacity - 1,
                        "update_time": currrent_time.timestamp(),
                    }
                ),
                ttl=self.refill_interval,
            )
            return True

        token = json.loads(data.decode("utf-8").replace("'", '"'))
        if token.get("token") > 0:
            self.db.add_token(
                key=ip,
                value=str(
                    {
                        "token": token.get("token") - 1,
                        "update_time": currrent_time.timestamp(),
                    }
                ),
                ttl=self.refill_interval,
            )
            return True
        else:
            return False
