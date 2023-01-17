from collections import defaultdict
import asyncio
import functools
from typing import Any, Awaitable, Callable


from .models import Entity, Event, WebHook, WebhookPattern


class HookSubscriber:

    def __init__(self, pattern: WebhookPattern, callback: Callable[..., Awaitable[None]], filter_pattern: dict | None = None, * args, **kwargs):
        self.pattern = pattern
        self.callback = callback
        self.filter_pattern = filter_pattern

    async def __call__(self, hook, *args: Any, **kwds: Any) -> Any:
        if self.filter_pattern:
            print("FILTERING")
            d = hook.data
            print([(d, d.get(k), k, v) for k, v in self.filter_pattern.items()], [d.get(k) == v for k, v in self.filter_pattern.items()])
            if not any([d.get(k) == v for k, v in self.filter_pattern.items()]):
                return

        await self.callback(*args, **kwds)


class WebhookHandlerPool:

    _subscribers: dict[WebhookPattern,
                       list[HookSubscriber]] = defaultdict(list)

    # def __init__(self, hook_type) -> None:
    #     self.hook_type = hook_type

    def _subscribe(self, subscriber: HookSubscriber):
        self._subscribers[subscriber.pattern].append(subscriber)

    def subscribe(self, entity: Entity | None = None, event: Event | None = None, filter_pattern=None):
        pattern = WebhookPattern(entity=entity, event=event)

        def decorator(wrapee):
            subscriber = HookSubscriber(pattern, wrapee, filter_pattern)
            self._subscribe(subscriber)

        return decorator

    # def unsubscribe(self, s)

    async def resolve(self, hook: WebHook):
        subscribers = self._subscribers.get(hook.pattern, [])
        tasks = list(subscriber(hook.body) for subscriber in subscribers)
        await asyncio.gather(*tasks)


HookSubscriberPool = WebhookHandlerPool()
