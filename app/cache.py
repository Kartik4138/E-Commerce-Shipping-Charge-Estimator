import redis.asyncio as redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

async def get_cached_data(key):
    data = await r.get(key)
    if data:
        return json.loads(data)
    return None

async def set_cached_data(key, data, ttl=1800):
    await r.setex(key, ttl, json.dumps(data))