import aioredis
from aioredis import Redis as Cache


def get_cache(url, decode_responses: bool = True) -> Cache:
    return aioredis.from_url(url, decode_responses=decode_responses)
