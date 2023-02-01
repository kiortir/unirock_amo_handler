import httpx
import os

root_path = os.environ.get("root_path", "/")

ALLOWED_HOSTS = [
    'testserver',
    'amocrm',
    '127.0.0.1'
]

_1c_RATE_LIMITER: None | int = None

client_1c = httpx.AsyncClient(timeout=15, limits=httpx.Limits(
    max_connections=_1c_RATE_LIMITER
))

