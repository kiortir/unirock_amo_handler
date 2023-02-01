import os
from typing import Any
from pydantic import BaseSettings, Field

from amocrm_api_client.token_provider import StandardTokenProviderFactory  # type: ignore    
from amocrm_api_client.token_provider.impl.standard.token_storage import (  # type: ignore    
    RedisTokenStorageImpl,
)

from ..redis_handler import redis_client

from dotenv import load_dotenv

dotenv_path = "/home/michael/projects/unirock_microservices/lead_orchestrator/.env"
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Settings(BaseSettings):

    BACKUP_FILE_PATH: str = ""
    ENCRYPTION_KEY: str = ""
    INTEGRATION_ID: str = ""
    SECRET_KEY: str = ""
    AUTH_CODE: str = ""
    BASE_URL: str = ""
    REDIRECT_URI: str = ""


settings: dict[str, Any] = {k.lower(): v for k, v in Settings().dict().items()}
settings["redis_client"] = redis_client

token_provider_factory = StandardTokenProviderFactory()
token_provider = token_provider_factory.get_instance(
    settings=settings, token_storage_class=RedisTokenStorageImpl
)
