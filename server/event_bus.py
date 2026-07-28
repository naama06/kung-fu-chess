from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(frozen=True)
class GameEvent:
    type: str
    data: dict[str, Any] = field(default_factory=dict)


Handler = Callable[[GameEvent], None]


class EventBus:

    def __init__(self):
        self._handlers: dict[str, list[Handler]] = {}

    def subscribe(self, event_type: str, handler: Handler) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event: GameEvent) -> None:
        for handler in self._handlers.get(event.type, []):
            handler(event)

        for handler in self._handlers.get("*", []):
            handler(event)
