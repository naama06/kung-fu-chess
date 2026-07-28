import asyncio
import json
import queue
import threading

import websockets

from server.protocol import snapshot_from_dict
from view.game_snapshot import GameSnapshot

HOST = "localhost"
PORT = 8765


class NetworkClient:

    def __init__(self):
        self.latest_snapshot: GameSnapshot | None = None
        self.player_name = ""
        self.player_color = ""
        self.connection_status = "disconnected"
        self.status_message = "Connecting..."
        self.game_over = False
        self._incoming: queue.Queue[dict] = queue.Queue()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._send_queue: asyncio.Queue | None = None

    def start(self, name: str) -> None:
        self.player_name = name
        self.connection_status = "connecting"
        self._thread = threading.Thread(target=self._run_thread, args=(name,), daemon=True)
        self._thread.start()

    def _run_thread(self, name: str) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._session(name))

    async def _session(self, name: str) -> None:
        uri = f"ws://{HOST}:{PORT}"
        self._send_queue = asyncio.Queue()

        try:
            async with websockets.connect(uri) as websocket:
                self.connection_status = "connected"
                await websocket.send(json.dumps({"type": "join", "name": name}))

                sender = asyncio.create_task(self._send_loop(websocket))
                try:
                    async for raw_message in websocket:
                        message = json.loads(raw_message)
                        self._handle_message(message)
                finally:
                    sender.cancel()

        except Exception as error:
            self.connection_status = "error"
            self.status_message = f"Connection failed: {error}"

    async def _send_loop(self, websocket) -> None:
        while True:
            message = await self._send_queue.get()
            await websocket.send(json.dumps(message))

    def _handle_message(self, message: dict) -> None:
        self._incoming.put(message)
        msg_type = message.get("type")

        if msg_type == "welcome":
            self.player_color = message.get("color", "")
            status = message.get("status", "")

            if status == "waiting":
                self.status_message = "Waiting for opponent..."
            elif status == "started":
                self.status_message = f"You are {self.player_color.upper()}. Game started!"
            elif status == "watching":
                self.status_message = "You are watching the game."

        elif msg_type == "state":
            self.latest_snapshot = snapshot_from_dict(message["snapshot"])
            self.game_over = self.latest_snapshot.game_over

            if self.connection_status == "connected" and self.status_message.startswith("Waiting"):
                self.status_message = "Waiting for opponent..."

        elif msg_type == "game_over":
            self.game_over = True
            self.status_message = "Game over!"

        elif msg_type == "error":
            self.status_message = message.get("message", "Unknown error")

    def poll(self) -> list[dict]:
        messages = []

        while not self._incoming.empty():
            messages.append(self._incoming.get_nowait())

        return messages

    def send_click(self, x: int, y: int) -> None:
        self._send({"type": "click", "x": x, "y": y})

    def send_jump(self, x: int, y: int) -> None:
        self._send({"type": "jump", "x": x, "y": y})

    def _send(self, message: dict) -> None:
        if self._loop is None or self._send_queue is None:
            return

        if self.connection_status != "connected":
            return

        if self.status_message.startswith("Waiting"):
            return

        asyncio.run_coroutine_threadsafe(
            self._send_queue.put(message),
            self._loop,
        )
