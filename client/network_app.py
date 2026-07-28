import sys
import time
from pathlib import Path

import cv2

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from client.network_client import NetworkClient
from view.game_snapshot import GameSnapshot
from view.renderer import Renderer

FRAME_MS = 16


class NetworkKungFuChessApp:

    def __init__(self, player_name: str):
        self.network = NetworkClient()
        self.renderer = Renderer()
        self.player_name = player_name
        self._running = True
        self._empty_snapshot = GameSnapshot(board_width=8, board_height=8)

    def run(self):
        print(f"Connecting as {self.player_name}...")
        self.network.start(self.player_name)

        cv2.namedWindow(Renderer.WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(Renderer.WINDOW_NAME, self._on_mouse)

        last_time = time.perf_counter()
        window_ready = False

        while self._running:
            now = time.perf_counter()
            elapsed_ms = int((now - last_time) * 1000)
            last_time = now

            self.network.poll()

            if elapsed_ms > 0:
                self.renderer.tick_animations(elapsed_ms)

            snapshot = self.network.latest_snapshot or self._empty_snapshot
            frame = self.renderer.render(snapshot)
            display = self._to_display_image(frame.img)
            self._draw_status_bar(display)

            if not window_ready and snapshot.board_width > 0:
                height, width = display.shape[:2]
                cv2.resizeWindow(Renderer.WINDOW_NAME, width, height)
                window_ready = True

            cv2.imshow(Renderer.WINDOW_NAME, display)

            key = cv2.waitKey(FRAME_MS) & 0xFF

            if key in (27, ord("q")):
                self._running = False

        cv2.destroyAllWindows()

    def _draw_status_bar(self, display):
        lines = [
            f"Player: {self.player_name} ({self.network.player_color or '...'})",
            self.network.status_message,
        ]

        y = 24

        for line in lines:
            cv2.putText(
                display,
                line,
                (16, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )
            y += 22

        if self.network.game_over:
            cv2.putText(
                display,
                "GAME OVER",
                (16, y + 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (80, 80, 255),
                2,
                cv2.LINE_AA,
            )

    def _on_mouse(self, event, x, y, _flags, _param):
        if event != cv2.EVENT_LBUTTONDOWN and event != cv2.EVENT_RBUTTONDOWN:
            return

        logical = self.renderer.pixel_to_logical(x, y)

        if logical is None:
            return

        logical_x, logical_y = logical

        if event == cv2.EVENT_RBUTTONDOWN:
            self.network.send_jump(logical_x, logical_y)
        else:
            self.network.send_click(logical_x, logical_y)

    @staticmethod
    def _to_display_image(image):
        if image.shape[2] == 4:
            return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        return image


def main():
    player_name = input("Username: ").strip() or "Player"
    NetworkKungFuChessApp(player_name).run()


if __name__ == "__main__":
    main()
