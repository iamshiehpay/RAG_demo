"""In-memory background upload jobs; subscribers can disconnect and replay progress."""

import asyncio
from collections.abc import AsyncIterator

from .events import Event


class UploadBusy(ValueError):
    """Only one Document operation can replace the active Document at a time."""


class IngestionJob:
    def __init__(self):
        self.events: list[Event] = []
        self.finished = False
        self.changed = asyncio.Condition()

    async def publish(self, event: Event):
        async with self.changed:
            self.events.append(event)
            self.finished = event.type in {"ready", "error"}
            self.changed.notify_all()

    async def subscribe(self) -> AsyncIterator[Event]:
        position = 0
        while True:
            async with self.changed:
                await self.changed.wait_for(
                    lambda position=position: position < len(self.events) or self.finished
                )
                pending = self.events[position:]
                position = len(self.events)
                finished = self.finished
            for event in pending:
                yield event
            if finished:
                return
