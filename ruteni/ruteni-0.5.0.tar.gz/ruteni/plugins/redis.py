import aioredis
from ruteni import configuration

REDIS_URL: str = configuration.get(
    "RUTENI_REDIS_URL", default="redis+unix:///run/redis/redis-server.sock"
)

redis = aioredis.from_url(REDIS_URL)
