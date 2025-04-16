import redis.asyncio as redis

REDIS_HOST = "localhost"
# REDIS_HOST = "messenger_redis"
REDIS_PORT = 6379
REDIS_DB = 0

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
