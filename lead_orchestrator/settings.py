import httpx

ALLOWED_HOSTS = [
    'testserver',
    'amocrm',
    '127.0.0.1'
]

_1c_RATE_LIMITER = None

client_1c = httpx.AsyncClient(timeout=15, limits=httpx.Limits(
    max_connections=_1c_RATE_LIMITER
))

