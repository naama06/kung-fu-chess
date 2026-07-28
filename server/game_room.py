import asyncio
from dataclasses import dataclass, field

from chess_io.board_parser import BoardParser
from controller import Controller
from server.event_bus import EventBus, GameEvent
from server.protocol import encode_message, snapshot_to_dict
from view.game_stats import GameStats
from view.motion_tracker import MotionTracker
from view.snapshot_builder import SnapshotBuilder

DEFAULT_BOARD = """
bR bN bB bQ bK bB bN bR
bP bP bP bP bP bP bP bP
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
wP wP wP wP wP wP wP wP
wR wN wB wQ wK wB wN wR
""".strip()

TICK_MS = 16


@dataclass
class PlayerSlot:
    name: str
    color: str
    connection: object


@dataclass
class GameRoom:
    bus: EventBus
    board_text: str = DEFAULT_BOARD
    controller: Controller = field(init=False)
    stats: GameStats = field(init=False)
    snapshot_builder: SnapshotBuilder = field(init=False)
    motion_tracker: MotionTracker = field(init=False)
    white_player: PlayerSlot | None = None
    black_player: PlayerSlot | None = None
    viewers: list[PlayerSlot] = field(default_factory=list)
    _started: bool = False
    _game_over_sent: bool = False
    _tick_task: asyncio.Task | None = field(default=None, repr=False)

    def __post_init__(self):
        board = BoardParser.parse(self.board_text)
        self.controller = Controller(board)
        self.stats = GameStats(white_name="White", black_name="Black")
        self.snapshot_builder = SnapshotBuilder(self.controller, self.stats)
        self.motion_tracker = MotionTracker()
        self._register_bus_handlers()

    def _register_bus_handlers(self):
        self.bus.subscribe("state_changed", self._on_state_changed)
        self.bus.subscribe("game_over", self._on_game_over_event)

    def start(self):
        if self._tick_task is None:
            self._tick_task = asyncio.create_task(self._tick_loop())

    async def stop(self):
        if self._tick_task is not None:
            self._tick_task.cancel()
            try:
                await self._tick_task
            except asyncio.CancelledError:
                pass
            self._tick_task = None

    def join(self, name: str, connection) -> dict:
        if self.white_player is None:
            self.white_player = PlayerSlot(name=name, color="white", connection=connection)
            self.stats.white_name = name
            self.bus.publish(GameEvent("player_joined", {"color": "white", "name": name}))
            self.bus.publish(GameEvent("state_changed", {}))
            return {"color": "white", "status": "waiting"}

        if self.black_player is None:
            self.black_player = PlayerSlot(name=name, color="black", connection=connection)
            self.stats.black_name = name
            self.bus.publish(GameEvent("player_joined", {"color": "black", "name": name}))
            self._start_game()
            return {"color": "black", "status": "started"}

        viewer = PlayerSlot(name=name, color="viewer", connection=connection)
        self.viewers.append(viewer)
        self.bus.publish(GameEvent("player_joined", {"color": "viewer", "name": name}))
        return {"color": "viewer", "status": "watching"}

    def _start_game(self):
        if self._started:
            return

        self._started = True
        self.bus.publish(
            GameEvent(
                "game_started",
                {
                    "white": self.stats.white_name,
                    "black": self.stats.black_name,
                },
            )
        )
        self.bus.publish(GameEvent("state_changed", {}))

    def handle_command(self, connection, command: str, args: list[str]) -> None:
        if not self._started:
            return

        if command in {"click", "jump", "wait"}:
            self.controller.execute_command(command, args)
            self._publish_state()

        if self.controller.engine.game_state.is_game_over() and not self._game_over_sent:
            self._game_over_sent = True
            self.bus.publish(GameEvent("game_over", {}))

    def _advance(self, ms: int):
        self.stats.tick(ms)
        self.motion_tracker.before_advance(self.controller.engine)
        self.controller.engine.advance_time(ms)
        self.motion_tracker.after_advance(self.controller.engine, self.stats)

        if self.controller.engine.game_state.is_game_over() and not self._game_over_sent:
            self._game_over_sent = True
            self.bus.publish(GameEvent("game_over", {}))

    def _publish_state(self):
        self.bus.publish(GameEvent("state_changed", {}))

    def _on_state_changed(self, _event: GameEvent):
        asyncio.create_task(self._broadcast_state())

    def _on_game_over_event(self, _event: GameEvent):
        asyncio.create_task(self._broadcast_message({"type": "game_over"}))

    async def _tick_loop(self):
        while True:
            self._advance(TICK_MS)
            if self.controller.engine.arbiter.has_active_motions() or (
                self.controller.engine.arbiter.airborne_jump is not None
            ):
                self._publish_state()
            await asyncio.sleep(TICK_MS / 1000)

    def _all_connections(self):
        connections = []

        if self.white_player is not None:
            connections.append(self.white_player.connection)

        if self.black_player is not None:
            connections.append(self.black_player.connection)

        connections.extend(viewer.connection for viewer in self.viewers)
        return connections

    async def _broadcast_state(self):
        snapshot = self.snapshot_builder.build()
        message = {
            "type": "state",
            "snapshot": snapshot_to_dict(snapshot),
        }
        await self._broadcast_message(message)

    async def _broadcast_message(self, message: dict):
        payload = encode_message(message)

        for connection in self._all_connections():
            try:
                await connection.send(payload)
            except Exception:
                pass
