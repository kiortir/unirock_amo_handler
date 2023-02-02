from datetime import datetime

from amocrm_api_client.make_amocrm_request.core.exceptions import (
    EntityNotFoundException,
)

from amocrm_api_client.models import CreateTask, Lead, Page, User
from fastapi import FastAPI, HTTPException, Response

from .amo.handler import (
    add_task,
    get_company_info,
    get_contacts,
    get_lead_info,
    get_leads,
    get_pipelines,
    get_tasks,
    get_users,
)
from .tools import request_to_wildcard_params
from .settings import root_path

app = FastAPI(root_path=root_path)
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


@app.get("/tasks/add")
async def add_task_(
    entity_id: int,
    entity_type: str,
    responsible_user_id: int,
    text: str,
    complete_till: datetime,
):
    await add_task(
        CreateTask(
            entity_id=entity_id,
            entity_type=entity_type,
            responsible_user_id=responsible_user_id,
            text=text,
            complete_till=complete_till,
        )
    )
    return Response(status_code=200)


def run(app_path="lead_orchestrator.main:app"):
    import uvicorn

    uvicorn.run(app_path, port=5000, log_level="info", reload=True)


if __name__ == "__main__":
    run("main:app")
