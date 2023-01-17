from .route_classes import QSEncodedRoute
from fastapi import Request, Response, APIRouter, BackgroundTasks
from .amo.models import WebHook
from .amo.webhook_handlers import HookSubscriberPool as pool

amo_router = APIRouter(route_class=QSEncodedRoute)


@amo_router.post("/tasks/webhook")
async def task_webhook(hook: WebHook, request: Request, background_tasks: BackgroundTasks):
    # from pprint import pprint
    # print("Hook recieved")
    # pprint(hook.dict())
    # pprint(hook.pattern)
    # pprint(hook.body)

    background_tasks.add_task(pool.resolve, hook)

    # print(request.headers)
