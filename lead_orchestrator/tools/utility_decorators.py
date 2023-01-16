from functools import wraps, reduce
from typing import Callable, TypeVar

T = TypeVar("T")


def timeit(foo):

    @wraps(foo)
    async def wrapper(*args, **kwargs):
        import time
        start = time.perf_counter()
        r = await foo(*args, **kwargs)
        end = time.perf_counter()
        print(f"fn: {foo.__name__}, elapsed: {end-start:.{3}f} s")
        return r

    return wrapper


def apply(o, fn: Callable):
    return fn(o)


def get_pipe(*fnlist: Callable) -> Callable:

    def pipe(o: T) -> T:
        return reduce(apply, fnlist, o)

    return pipe
