from typing import Callable
from urllib.parse import unquote

import qsparser
from fastapi import Request
from .utility_decorators import get_pipe
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from starlette.types import Receive, Scope, Send


class PostTrustedHostMiddleware(TrustedHostMiddleware):

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope.get('method') != "POST":
            return await self.app(scope, receive, send)

        return await super().__call__(scope, receive, send)


def request_to_wildcard_params(endpoint_fn: Callable):

    parse = get_pipe(str, unquote, qsparser.parse)

    async def wrapper(request: Request):

        params = request.query_params
        if params:
            params = parse(params)
        return await endpoint_fn(params)

    wrapper.__name__ = endpoint_fn.__name__
    return wrapper
