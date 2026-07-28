from server.event_bus import GameEvent
from server.game_room import GameRoom
from server.protocol import decode_message, encode_message


async def handle_client(websocket, room: GameRoom):
    joined = False

    try:
        async for raw_message in websocket:
            message = decode_message(raw_message)
            msg_type = message.get("type")

            if msg_type == "join":
                name = str(message.get("name", "Player"))
                result = room.join(name, websocket)
                joined = True

                await websocket.send(
                    encode_message(
                        {
                            "type": "welcome",
                            "name": name,
                            **result,
                        }
                    )
                )

                if result["status"] in {"started", "watching"}:
                    room.bus.publish(GameEvent("state_changed", {}))

                continue

            if not joined:
                await websocket.send(
                    encode_message(
                        {
                            "type": "error",
                            "message": "Send join before other commands.",
                        }
                    )
                )
                continue

            if msg_type == "click":
                room.handle_command(
                    websocket,
                    "click",
                    [str(message["x"]), str(message["y"])],
                )

            elif msg_type == "jump":
                room.handle_command(
                    websocket,
                    "jump",
                    [str(message["x"]), str(message["y"])],
                )

            elif msg_type == "wait":
                room.handle_command(
                    websocket,
                    "wait",
                    [str(message["ms"])],
                )

            else:
                await websocket.send(
                    encode_message(
                        {
                            "type": "error",
                            "message": f"Unknown message type: {msg_type}",
                        }
                    )
                )

    except Exception:
        pass
