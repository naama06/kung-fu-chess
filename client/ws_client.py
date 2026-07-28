import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import websockets

HOST = "localhost"
PORT = 8765


async def listen_for_messages(websocket):
    async for raw_message in websocket:
        message = json.loads(raw_message)
        msg_type = message.get("type")

        if msg_type == "welcome":
            print(
                f"[server] Welcome {message['name']}! "
                f"color={message['color']} status={message['status']}"
            )

        elif msg_type == "state":
            snapshot = message["snapshot"]
            piece_count = len(snapshot.get("pieces", []))
            print(
                f"[state] pieces={piece_count} "
                f"score W:{snapshot['white_score']} B:{snapshot['black_score']} "
                f"game_over={snapshot['game_over']}"
            )

        elif msg_type == "game_over":
            print("[server] Game over!")

        elif msg_type == "error":
            print(f"[error] {message.get('message')}")

        else:
            print(f"[server] {message}")


async def send_commands(websocket):
    while True:
        command = await asyncio.to_thread(input, "> ")

        if command in {"quit", "exit", "q"}:
            break

        parts = command.split()

        if not parts:
            continue

        action = parts[0]

        if action == "click" and len(parts) == 3:
            message = {
                "type": "click",
                "x": int(parts[1]),
                "y": int(parts[2]),
            }
            await websocket.send(json.dumps(message))

        elif action == "jump" and len(parts) == 3:
            message = {
                "type": "jump",
                "x": int(parts[1]),
                "y": int(parts[2]),
            }
            await websocket.send(json.dumps(message))

        elif action == "wait" and len(parts) == 2:
            message = {
                "type": "wait",
                "ms": int(parts[1]),
            }
            await websocket.send(json.dumps(message))

        else:
            print("Commands: click X Y | jump X Y | wait MS | quit")


async def main():
    name = input("Username: ").strip() or "Player"

    async with websockets.connect(f"ws://{HOST}:{PORT}") as websocket:
        await websocket.send(json.dumps({"type": "join", "name": name}))

        listener = asyncio.create_task(listen_for_messages(websocket))
        sender = asyncio.create_task(send_commands(websocket))

        done, pending = await asyncio.wait(
            {listener, sender},
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
