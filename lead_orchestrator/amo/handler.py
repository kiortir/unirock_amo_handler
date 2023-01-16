import ujson
from amocrm_api_client.model_builder.ModelBuilderImpl import ModelBuilderImpl
from amocrm_api_client.make_amocrm_request.core.exceptions import EntityNotFoundException
import asyncio
from functools import wraps

from amocrm_api_client.models.Filters import LeadListFilter, CustomersListFilter, TaskListFilter
from amocrm_api_client.models import Lead, Page, User, CreateTask
from amocrm_api_client.models.lead.AddNote import NoteTypes


from . import client
from ..tools.utility_decorators import timeit
from ..redis_handler.cache import AsyncRedisCache


async def get_company_info():
    amo_client = await client()
    info = await amo_client.account.get_info()
    return info


async def get_lead_info(lead_id: int):
    amo_client = await client()
    info = await amo_client.leads.get_by_id(lead_id)
    return info


async def get_leads(filter=None, **kwargs) -> Page[Lead]:
    amo_client = await client()
    if filter:
        filter = LeadListFilter(**filter)

    info: Page[Lead] = Page(
        _page=kwargs.get('page', 1),
        _total_items=0,
        _page_count=None,
        _embedded=[])

    try:
        info = await amo_client.leads.get_page(filter=filter, **kwargs)
    except EntityNotFoundException:
        ...
    return info

@timeit
@AsyncRedisCache(ttl=60 * 60 * 24, namespace="pipelines")
async def get_pipelines():
    amo_client = await client()
    info = await amo_client.pipelines.get_all()
    return info


async def get_contacts(filter=None, recursive=False, **kwargs):
    amo_client = await client()
    if filter is not None:
        filter = CustomersListFilter(**filter)

    try:
        info = await amo_client.contacts.get_page(filter=filter, **kwargs)

    except EntityNotFoundException:
        info = Page(
            _page=kwargs.get('page', 1),
            _total_items=0,
            _page_count=None,
            _embedded=[])
    return info


async def get_user(user_id: int) -> User | None:
    users = await get_users()
    for user in users.embedded:
        if user.id == user_id:
            return user

    return None

@timeit
@AsyncRedisCache(ttl=60 * 60 * 24, namespace="users_cache")
async def get_users(recursive=True, **kwargs) -> Page[User]:
    amo_client = await client()
    info = await amo_client.users.get_page(**kwargs)
    if recursive and info.page_count and info.page_count > info.page:
        kwargs["page"] = info.page + 1
        next_page = await get_users(recursive=recursive, **kwargs)
        info.embedded.extend(next_page.embedded)
    return info

async def get_tasks(limit: int = 250, page: int = 1, filter_: TaskListFilter | None = None):
    amo_client = await client()
    return await amo_client.tasks.get_page(limit=limit, page=page, filter=filter_)


async def add_task(task: CreateTask):
    amo_client = await client()
    await amo_client.tasks.add(task)


async def create_task_measurement(webhook):
    ...
