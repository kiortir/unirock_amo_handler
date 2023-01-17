from .route_classes import QSEncodedRoute
from fastapi import Request, Response, APIRouter
from .amo.models import WebHook

amo_router = APIRouter(route_class=QSEncodedRoute)


@amo_router.post("/tasks/webhook")
async def task_webhook(hook: WebHook, request: Request):
    print("Hook recieved")
    print(await request.json())
    print(request.headers)
    print(hook)

    return Response(status_code=200)
