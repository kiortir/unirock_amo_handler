from .webhook_handlers import HookSubscriberPool as pool
from .models import Entity, Event
from .webhook_models import LeadData

import asyncio
@pool.subscribe(
    entity=Entity.LEAD,
    event=Event.STATUS,
    filter_pattern={
        "id": 26066553
    }
)
async def set_task(*args):
    await asyncio.sleep(2)
    print("executing_subscribed_task")


@pool.subscribe(
    entity=Entity.LEAD,
    event=Event.STATUS
)
async def set_task3213(*args):
    print("executing_subscribed_task2")


@pool.subscribe(
    entity=Entity.LEAD,
    event=Event.STATUS
)
async def weqwewqe(*args):
    print("executing_subscribed_task43")
