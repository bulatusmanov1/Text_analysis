from httpx import AsyncClient

import asyncio
import datetime as dt
from functools import wraps

_background_tasks = set()


class RateLimitedClient(AsyncClient):
    """httpx.AsyncClient with a rate limit."""

    def __init__(self, interval: float, count=1, **kwargs):
        self.interval = interval
        self.semaphore = asyncio.Semaphore(count)
        super().__init__(**kwargs)

    def _schedule_semaphore_release(self):
        wait = asyncio.create_task(asyncio.sleep(self.interval))
        _background_tasks.add(wait)

        def wait_cb(task):
            self.semaphore.release()
            _background_tasks.discard(task)

        wait.add_done_callback(wait_cb)

    @wraps(AsyncClient.send)
    async def send(self, *args, **kwargs):
        await self.semaphore.acquire()
        send = asyncio.create_task(super().send(*args, **kwargs))
        self._schedule_semaphore_release()
        return await send
