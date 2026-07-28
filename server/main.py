import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import websockets

from server.event_bus import EventBus
from server.game_room import GameRoom
from server.ws_handler import handle_client

HOST = "localhost"
PORT = 8765


async def main():
    bus = EventBus()
    room = GameRoom(bus=bus)
    room.start()

    async with websockets.serve(
        lambda websocket: handle_client(websocket, room),
        HOST,
        PORT,
    ):
        print(f"KungFu Chess server running on ws://{HOST}:{PORT}")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
