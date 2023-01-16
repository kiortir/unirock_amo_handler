import os

from redis import asyncio as aioredis


redis_client = aioredis.Redis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=6379
)
    
