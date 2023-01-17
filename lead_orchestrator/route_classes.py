from urllib.parse import unquote
from typing import Callable

import qsparser
import ujson
from fastapi import Request, Response
from fastapi.routing import APIRoute


class QSRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            body = qsparser.parse(unquote(body.decode("utf-8")))
            self._body = ujson.dumps(body, encode_html_chars=False, ensure_ascii=False).encode()
        return self._body


class QSEncodedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = QSRequest(request.scope, request.receive)
            print(await request.body())
            return await original_route_handler(request)

        return custom_route_handler
