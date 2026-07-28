from server.event_bus import EventBus, GameEvent


def test_event_bus_calls_subscribers():
    bus = EventBus()
    received = []

    bus.subscribe("state_changed", lambda event: received.append(event.type))
    bus.publish(GameEvent("state_changed", {"pieces": 32}))

    assert received == ["state_changed"]


def test_event_bus_does_not_call_other_handlers():
    bus = EventBus()
    received = []

    bus.subscribe("game_over", lambda event: received.append(event.type))
    bus.publish(GameEvent("state_changed", {}))

    assert received == []
