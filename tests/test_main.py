from lead_orchestrator.main import app
from fastapi.testclient import TestClient
import json
import pytest
import asyncio
from httpx import AsyncClient

client = TestClient(app)
pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_webhook():
    with open('/home/michael/projects/lead_orchestrator/tests/testhook.json', "r", encoding='utf-8') as f:
        hook = json.load(f)

    async with AsyncClient(app=app) as ac:
        
        responses = await asyncio.gather(*[ac.post('http://127.0.0.1:5000/webhook', json=hook) for _ in range(15)])

    print(responses)