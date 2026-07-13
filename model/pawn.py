from model.piece import Piece
from model.position import Position


class Pawn(Piece):

    def __init__(self, color):
        super().__init__(piece_type="pawn", color=color)

    @property
    def symbol(self):
        return "P"

    def is_valid_move(self, board, start_pos, end_pos):
        if start_pos == end_pos:
            return False

        direction = -1 if self.color == "white" else 1

        row_diff = end_pos.row - start_pos.row
        col_diff = end_pos.col - start_pos.col

        target = board.get_piece(end_pos)

        if col_diff == 0 and row_diff == direction:
            return target is None

        if (
            col_diff == 0
            and row_diff == 2 * direction
            and self._is_start_row(board, start_pos.row)
        ):
            if target is not None:
                return False

            middle = Position(start_pos.row + direction, start_pos.col)

            return board.get_piece(middle) is None

        if abs(col_diff) == 1 and row_diff == direction:
            return target is not None and target.color != self.color

        return False

    def _is_start_row(self, board, row):
        if self.color == "white":
            return row == board.height - 1

        return row == 0
