import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    REDIS_SERVER = os.getenv("REDIS_SERVER")
