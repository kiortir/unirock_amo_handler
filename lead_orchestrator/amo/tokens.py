import pathlib
from typing import Any

from amocrm_api_client.token_provider import StandardTokenProviderFactory
from amocrm_api_client.token_provider.impl.standard.token_storage import \
    RedisTokenStorageImpl
from dotenv import dotenv_values

from ..redis_handler import redis_client

SETTINGS_ENV_PATH = (pathlib.Path(__file__).parent /
                     '.env.amo_settings').resolve()
SETTINGS_ENV = dotenv_values(SETTINGS_ENV_PATH)

settings: dict[str, Any] = {k.lower(): v for k, v in SETTINGS_ENV.items()}
settings["redis_client"] = redis_client

token_provider_factory = StandardTokenProviderFactory()
token_provider = token_provider_factory.get_instance(
    settings=settings, token_storage_class=RedisTokenStorageImpl)
