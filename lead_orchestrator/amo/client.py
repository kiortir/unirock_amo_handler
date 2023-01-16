import asyncio
from amocrm_api_client import AmoCrmApiClient
from amocrm_api_client import AmoCrmApiClientConfig
from amocrm_api_client import create_amocrm_api_client
from . import tokens
    


class AmoClient:

    def __init__(self):
        self.dispatcher = self._dispatcher()


    async def _dispatcher(self):

        amo_client: AmoCrmApiClient = create_amocrm_api_client(
            token_provider=tokens.token_provider,
            config=AmoCrmApiClientConfig(base_url=tokens.settings['base_url'] or ""))
        await amo_client.initialize()

        while True:
            yield amo_client

    async def get_instance(self):
        return await anext(self.dispatcher)

    def __call__(self):
        return self.get_instance()