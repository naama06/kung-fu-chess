import sys
import time

import cv2

from chess_io.board_parser import BoardParser
from controller import Controller
from view.game_stats import GameStats
from view.motion_tracker import MotionTracker
from view.renderer import Renderer
from view.snapshot_builder import SnapshotBuilder

FRAME_MS = 16
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


class KungFuChessApp:

    def __init__(self, board_text: str = DEFAULT_BOARD):
        board = BoardParser.parse(board_text)
        self.controller = Controller(board)
        self.stats = GameStats(white_name="White", black_name="Black")
        self.snapshot_builder = SnapshotBuilder(self.controller, self.stats)
        self.renderer = Renderer()
        self.motion_tracker = MotionTracker()
        self._running = True

    def run(self):
        cv2.namedWindow(Renderer.WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(Renderer.WINDOW_NAME, self._on_mouse)

        last_time = time.perf_counter()
        window_ready = False

        while self._running:
            now = time.perf_counter()
            elapsed_ms = int((now - last_time) * 1000)
            last_time = now

            if elapsed_ms > 0:
                self._advance(elapsed_ms)

            snapshot = self.snapshot_builder.build()
            frame = self.renderer.render(snapshot)
            display = self._to_display_image(frame.img)

            if not window_ready:
                height, width = display.shape[:2]
                cv2.resizeWindow(Renderer.WINDOW_NAME, width, height)
                window_ready = True

            cv2.imshow(Renderer.WINDOW_NAME, display)

            key = cv2.waitKey(FRAME_MS) & 0xFF

            if key in (27, ord("q")):
                self._running = False

        cv2.destroyAllWindows()

    def _advance(self, ms: int):
        self.stats.tick(ms)
        self.renderer.tick_animations(ms)
        self.motion_tracker.before_advance(self.controller.engine)
        self.controller.engine.advance_time(ms)
        self.motion_tracker.after_advance(self.controller.engine, self.stats)

    def _on_mouse(self, event, x, y, _flags, _param):
        if event != cv2.EVENT_LBUTTONDOWN and event != cv2.EVENT_RBUTTONDOWN:
            return

        logical = self.renderer.pixel_to_logical(x, y)

        if logical is None:
            return

        logical_x, logical_y = logical
        command = "jump" if event == cv2.EVENT_RBUTTONDOWN else "click"
        self.controller.execute_command(
            command,
            [str(logical_x), str(logical_y)],
        )

    @staticmethod
    def _to_display_image(image):
        if image.shape[2] == 4:
            return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        return image


def main():
    board_text = DEFAULT_BOARD

    if len(sys.argv) > 1:
        board_text = sys.argv[1]

    KungFuChessApp(board_text).run()


if __name__ == "__main__":
    main()
