import pickle
import uuid
from functools import wraps
from typing import Callable, Any

import ujson
from redis import asyncio as aioredis

from ..tools.utility_decorators import timeit
from . import redis_client as _client


class AsyncRedisCache:

    """
        ``ttl`` - in seconds
    """

    def __init__(
        self,
        ttl: float | None = 60.0,
        namespace: str | None = None,
        redis_client: aioredis.Redis = _client,
        serializer: Callable[[Any], str] = ujson.dumps,
    ):
        self.client = redis_client
        self.ttl = ttl
        self.namespace = namespace or uuid.uuid4().hex
        self.serializer = serializer

    async def get_key(self, fn_name, args, kwargs):
        serialized = self.serializer([args, kwargs])
        return f"{self.namespace}:{fn_name}:{serialized}"

    def __call__(self, fn: Callable):

        fn.__doc__ = str(fn.__doc__) + """
            this function is cached

            :param __force: Use to force cache update
            :type __force: bool
        """

        @wraps(fn)
        async def wrapper(*args, **kwargs):
            key = await self.get_key(fn.__name__, args, kwargs)
            if not await self.client.lock(f"lock:{key}").locked():
                cached = await self.client.get(key)
            else:
                async with self.client.lock(f"lock:{key}"):
                    cached = await self.client.get(key)
            if kwargs.pop("__force", False) or cached is None:
                async with self.client.lock(f"lock:{key}"):
                    v = await fn(*args, **kwargs)
                    await self.client.set(key, pickle.dumps(v), ex=self.ttl)
                    return v
            return pickle.loads(cached)

        return wrapper

    async def flush(self):
        async for key in self.client.scan_iter(f"{self.namespace}:*"):
            await self.client.delete(key)
