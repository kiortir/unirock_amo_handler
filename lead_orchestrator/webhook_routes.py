from .route_classes import QSEncodedRoute
from fastapi import Request, Response, APIRouter
from .amo.models import WebHook

amo_router = APIRouter(route_class=QSEncodedRoute)


@amo_router.post("/tasks/webhook", response_model=WebHook)
async def task_webhook(hook: WebHook, request: Request):
    print("Hook recieved")
    print(hook)
    print(request.headers)

    return hook
