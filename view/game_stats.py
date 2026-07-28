from view.piece_assets import PIECE_LETTERS, PIECE_VALUES, square_label


class GameStats:

    def __init__(self, white_name="White", black_name="Black"):
        self.white_name = white_name
        self.black_name = black_name
        self.white_score = 0
        self.black_score = 0
        self.white_moves: list[str] = []
        self.black_moves: list[str] = []
        self._game_ms = 0

    def tick(self, ms: int):
        self._game_ms += ms

    def record_capture(self, capturer_color: str, captured_piece_type: str):
        points = PIECE_VALUES.get(captured_piece_type, 0)

        if capturer_color == "white":
            self.white_score += points
        else:
            self.black_score += points

    def record_move(
        self,
        color: str,
        piece_type: str,
        dest_col: int,
        dest_row: int,
        captured: bool,
    ):
        letter = "" if piece_type == "pawn" else PIECE_LETTERS[piece_type]
        capture_mark = "x" if captured else ""
        notation = f"{letter}{capture_mark}{square_label(dest_col, dest_row)}"
        seconds = self._game_ms / 1000
        entry = f"{seconds:5.1f}s  {notation}"

        if color == "white":
            self.white_moves.append(entry)
        else:
            self.black_moves.append(entry)
