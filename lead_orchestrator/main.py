from datetime import datetime
from fastapi import FastAPI, HTTPException, Response, BackgroundTasks, Request

from amocrm_api_client.models import Lead, Page, User, CreateTask
from amocrm_api_client.make_amocrm_request.core.exceptions import \
    EntityNotFoundException

from . import settings
from .settings import client_1c
from .amo.handler import (get_company_info, get_contacts, get_lead_info,
                          get_leads, get_pipelines, get_users, get_tasks, add_task, create_task_measurement)
from .amo.models import WebHook
from .tools import request_to_wildcard_params
from .tools.fastapi_decorators import PostTrustedHostMiddleware
from .tools.utility_decorators import timeit

app = FastAPI()

# app.add_middleware(PostTrustedHostMiddleware,
#                    allowed_hosts=settings.ALLOWED_HOSTS)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/company")
async def company_info():
    info = await get_company_info()
    return info.dict()


@app.get("/leads", response_model=Page[Lead])
@request_to_wildcard_params
async def leads(params: dict):

    info = await get_leads(**params)
    return info


@app.get("/leads/{lead_id}", response_model=Lead)
async def lead_info(lead_id: int):
    try:
        info = await get_lead_info(lead_id)
    except EntityNotFoundException:
        raise HTTPException(status_code=404, detail="lead not found")
    return info


@app.get("/pipes/")
async def pipelines():
    info = await get_pipelines()

    return info


@app.get("/contacts/")
@request_to_wildcard_params
async def contacts(params: dict):
    info = await get_contacts(**params)

    return info


@app.get("/users", response_model=Page[User])
async def users():
    info = await get_users()
    return info


@app.get("/settask")
async def test_message():
    return await get_tasks()
    return Response(status_code=201)


@app.get("/tasks/add")
async def add_task_():
    await add_task(CreateTask(
        entity_id=26066553,
        entity_type="leads",
        responsible_user_id=2852878,
        text="tetsts",
        complete_till=datetime(2023, 2, 1, 12, 36)
    ))


@app.post("/webhook")
async def webhook(hook: WebHook, background_tasks: BackgroundTasks):
    print("Hook recieved")
    background_tasks.add_task(
        client_1c.post, "https://webhook.site/2f469d63-36c6-41af-9527-bf84cf6da3c9", json=hook.dict())

    return Response(status_code=200)


@app.post("/tasks/webhook")
async def task_webhook(request: Request):
    print("Hook recieved")
    print(request.body())
    print(request.client)

    return Response(status_code=200)

# @app.post("/tasks/webhook")
# async def task_webhook(hook: WebHook, background_tasks: BackgroundTasks):
#     print("Hook recieved")
#     print(hook.json())

#     background_tasks.add_task(
#         create_task_measurement, hook)

#     return Response(status_code=200)


def run(app_path="lead_orchestrator.main:app"):
    import uvicorn
    uvicorn.run(app_path, port=5000, log_level="info", reload=True)


if __name__ == "__main__":
    run("main:app")
