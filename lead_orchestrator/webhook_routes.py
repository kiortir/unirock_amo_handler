from .route_classes import QSEncodedRoute
from fastapi import Request, Response, APIRouter


amo_router = APIRouter(route_class=QSEncodedRoute)


@amo_router.post("/tasks/webhook")
async def task_webhook(request: Request):
    print("Hook recieved")
    print(await request.body())
    print(request.client)
    print(await request.json())

    return Response(status_code=200)
