from dotenv import load_dotenv
from redis.asyncio import Redis as async_redis
import logging
import os
load_dotenv()

logs_folder = "./logs"
os.makedirs(logs_folder, exist_ok=True)
logging.basicConfig(filename=f"{logs_folder}/app.log",filemode="a",level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
)
logging.getLogger("watchfiles").setLevel(logging.WARNING)


class Settings:
    origins = [origin.strip().rstrip("/") for origin in os.getenv("origins").split(",")]
    CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")
    DATABASE_URL = os.getenv("DATABASE_URL")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    
    def get_async_redis(self):
        return async_redis(host=self.REDIS_HOST, port=self.REDIS_PORT, decode_responses=True)
    
    def get_logger(self, name):
        return logging.getLogger(name)


settings = Settings()


