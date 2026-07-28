import cv2
import numpy as np

from graphics.img import Img
from view.animation_player import AnimationPlayer
from view.assets_config import (
    BOARD_PADDING,
    SIDE_PANEL_WIDTH,
    STATIC_ANIM_STATES,
    TARGET_CELL_SIZE,
    TOP_TITLE_HEIGHT,
)
from view.game_snapshot import GameSnapshot, PieceView
from view.sprite_loader import SpriteLoader
from view import ui_theme as theme


class Renderer:

    WINDOW_NAME = "KungFu Chess"

    def __init__(self):
        self.sprite_loader = SpriteLoader()
        self._players: dict[str, AnimationPlayer] = {}
        self._board_offset = (0, 0)
        self._cell_size = TARGET_CELL_SIZE
        self._board_pixel_w = 0
        self._board_pixel_h = 0

    def window_size(self, snapshot: GameSnapshot) -> tuple[int, int]:
        cell = TARGET_CELL_SIZE
        board_w = snapshot.board_width * cell
        board_h = snapshot.board_height * cell
        width = SIDE_PANEL_WIDTH * 2 + board_w + BOARD_PADDING * 2
        height = TOP_TITLE_HEIGHT + board_h + BOARD_PADDING * 2
        return width, height

    def board_origin(self) -> tuple[int, int]:
        return self._board_offset

    def pixel_to_logical(self, x: int, y: int) -> tuple[int, int] | None:
        ox, oy = self._board_offset

        if not (
            ox <= x < ox + self._board_pixel_w
            and oy <= y < oy + self._board_pixel_h
        ):
            return None

        col = int((x - ox) / self._cell_size)
        row = int((y - oy) / self._cell_size)
        logical_x = col * 100 + 50
        logical_y = row * 100 + 50
        return logical_x, logical_y

    def render(self, snapshot: GameSnapshot) -> Img:
        window_w, window_h = self.window_size(snapshot)
        cell = TARGET_CELL_SIZE

        self._cell_size = cell
        self._board_pixel_w = snapshot.board_width * cell
        self._board_pixel_h = snapshot.board_height * cell

        board_x = SIDE_PANEL_WIDTH + BOARD_PADDING
        board_y = TOP_TITLE_HEIGHT + BOARD_PADDING
        self._board_offset = (board_x, board_y)

        canvas = Img()
        canvas.img = np.zeros((window_h, window_w, 4), dtype=np.uint8)
        canvas.img[:, :] = theme.BG

        self._draw_title_bar(canvas, window_w)
        self._draw_player_panel(
            canvas,
            x=0,
            y=TOP_TITLE_HEIGHT,
            width=SIDE_PANEL_WIDTH,
            height=window_h - TOP_TITLE_HEIGHT,
            snapshot=snapshot,
            color="black",
        )
        self._draw_player_panel(
            canvas,
            x=window_w - SIDE_PANEL_WIDTH,
            y=TOP_TITLE_HEIGHT,
            width=SIDE_PANEL_WIDTH,
            height=window_h - TOP_TITLE_HEIGHT,
            snapshot=snapshot,
            color="white",
        )
        self._draw_board(canvas, snapshot, board_x, board_y, cell)

        for piece in snapshot.pieces:
            self._draw_piece(canvas, piece)

        if snapshot.game_over:
            self._draw_game_over(canvas, board_x, board_y)

        return canvas

    def _draw_title_bar(self, canvas: Img, window_w: int):
        canvas.img[0:TOP_TITLE_HEIGHT, :] = theme.TITLE_BAR
        title = "KUNG FU CHESS"
        text_x = window_w // 2 - len(title) * 9
        canvas.put_text(
            title,
            max(text_x, 16),
            36,
            0.85,
            color=theme.TEXT_PRIMARY,
            thickness=2,
        )

    def _draw_board(
        self,
        canvas: Img,
        snapshot: GameSnapshot,
        board_x: int,
        board_y: int,
        cell: int,
    ):
        rows = snapshot.board_height
        cols = snapshot.board_width

        for row in range(rows):
            for col in range(cols):
                x1 = board_x + col * cell
                y1 = board_y + row * cell
                square_color = (
                    theme.BOARD_LIGHT
                    if (row + col) % 2 == 0
                    else theme.BOARD_DARK
                )
                cv2.rectangle(
                    canvas.img,
                    (x1, y1),
                    (x1 + cell, y1 + cell),
                    square_color,
                    -1,
                )

        border = 3
        cv2.rectangle(
            canvas.img,
            (board_x - border, board_y - border),
            (board_x + cols * cell + border, board_y + rows * cell + border),
            theme.BOARD_BORDER,
            border,
            lineType=cv2.LINE_AA,
        )

    def _draw_player_panel(
        self,
        canvas: Img,
        x: int,
        y: int,
        width: int,
        height: int,
        snapshot: GameSnapshot,
        color: str,
    ):
        panel = canvas.img[y : y + height, x : x + width]
        panel[:, :] = theme.PANEL_BG

        accent = theme.BLACK_ACCENT if color == "black" else theme.WHITE_ACCENT
        cv2.rectangle(
            canvas.img,
            (x, y),
            (x + width, y + height),
            theme.PANEL_BORDER,
            1,
        )
        cv2.rectangle(
            canvas.img,
            (x + 12, y + 12),
            (x + width - 12, y + 118),
            accent,
            2,
            lineType=cv2.LINE_AA,
        )

        if color == "black":
            label = "BLACK"
            name = snapshot.black_name
            score = snapshot.black_score
            moves = snapshot.black_moves
        else:
            label = "WHITE"
            name = snapshot.white_name
            score = snapshot.white_score
            moves = snapshot.white_moves

        canvas.put_text(
            label,
            x + 24,
            y + 40,
            0.55,
            color=theme.TEXT_MUTED,
            thickness=1,
        )
        canvas.put_text(
            name,
            x + 24,
            y + 68,
            0.75,
            color=theme.TEXT_PRIMARY,
            thickness=2,
        )
        canvas.put_text(
            str(score),
            x + 24,
            y + 108,
            1.4,
            color=theme.TEXT_SCORE,
            thickness=3,
        )
        canvas.put_text(
            "points",
            x + 24 + len(str(score)) * 22 + 8,
            y + 108,
            0.5,
            color=theme.TEXT_MUTED,
            thickness=1,
        )

        canvas.put_text(
            "Moves",
            x + 24,
            y + 148,
            0.6,
            color=theme.TEXT_MUTED,
            thickness=1,
        )

        move_y = y + 176
        for index, move in enumerate(reversed(moves[-10:])):
            row_color = (
                theme.MOVE_ROW_EVEN if index % 2 == 0 else theme.MOVE_ROW_ODD
            )
            cv2.rectangle(
                canvas.img,
                (x + 16, move_y - 14),
                (x + width - 16, move_y + 6),
                row_color,
                -1,
            )
            canvas.put_text(
                move,
                x + 24,
                move_y,
                0.42,
                color=theme.TEXT_PRIMARY,
                thickness=1,
            )
            move_y += 24

    def _draw_piece(self, canvas: Img, piece: PieceView):
        piece_size = int(self._cell_size * 0.82)
        frames = self.sprite_loader.get_frames(
            piece.color,
            piece.piece_type,
            piece.anim_state,
            (piece_size, piece_size),
        )
        meta = self.sprite_loader.get_animation_meta(
            piece.color,
            piece.piece_type,
            piece.anim_state,
        )
        graphics = meta.get("graphics", {})

        if piece.anim_state in STATIC_ANIM_STATES:
            frame = frames[0]
        else:
            player = self._player_for(piece, len(frames), graphics)
            frame = frames[player.current_index()]

        ox, oy = self._board_offset
        center_x = ox + int((piece.col + 0.5) * self._cell_size)
        center_y = oy + int((piece.row + 0.5) * self._cell_size)
        half = piece_size // 2
        draw_x = center_x - half
        draw_y = center_y - half

        if piece.is_selected:
            self._draw_selection(canvas, center_x, center_y)

        frame.draw_on(canvas, draw_x, draw_y)

    def _player_for(
        self,
        piece: PieceView,
        frame_count: int,
        graphics: dict,
    ) -> AnimationPlayer:
        key = (
            f"{piece.color}:{piece.piece_type}:"
            f"{piece.row:.2f}:{piece.col:.2f}:{piece.anim_state}"
        )

        if key not in self._players:
            self._players[key] = AnimationPlayer(
                frame_count=frame_count,
                fps=float(graphics.get("frames_per_sec", 6)),
                loop=bool(graphics.get("is_loop", True)),
            )

        return self._players[key]

    def tick_animations(self, ms: int):
        for key, player in self._players.items():
            if any(state in key for state in STATIC_ANIM_STATES):
                continue

            player.tick(ms)

    def _draw_selection(self, canvas: Img, center_x: int, center_y: int):
        radius = int(self._cell_size * 0.42)
        cv2.circle(
            canvas.img,
            (center_x, center_y),
            radius,
            theme.SELECTION,
            2,
            lineType=cv2.LINE_AA,
        )

    def _draw_game_over(self, canvas: Img, board_x: int, board_y: int):
        overlay = canvas.img[
            board_y : board_y + self._board_pixel_h,
            board_x : board_x + self._board_pixel_w,
        ]
        dark = np.zeros_like(overlay)
        dark[:, :] = (20, 20, 20, 180)
        alpha = dark[:, :, 3:4] / 255.0
        overlay[:, :, :3] = (
            (1 - alpha) * overlay[:, :, :3] + alpha * dark[:, :, :3]
        ).astype(np.uint8)

        canvas.put_text(
            "GAME OVER",
            board_x + self._board_pixel_w // 2 - 120,
            board_y + self._board_pixel_h // 2,
            1.4,
            color=theme.GAME_OVER,
            thickness=3,
        )
