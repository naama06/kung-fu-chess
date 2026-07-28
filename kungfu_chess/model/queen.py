from model.piece import Piece
from model.position import Position


class Queen(Piece):

    def __init__(self, color):
        super().__init__(piece_type="queen", color=color)

    @property
    def symbol(self):
        return "Q"

    def is_valid_move(self, board, start_pos, end_pos):
        if start_pos == end_pos:
            return False

        row_diff = abs(end_pos.row - start_pos.row)
        col_diff = abs(end_pos.col - start_pos.col)

        is_straight = start_pos.row == end_pos.row or start_pos.col == end_pos.col
        is_diagonal = row_diff == col_diff

        if not is_straight and not is_diagonal:
            return False

        step_r = 0 if row_diff == 0 else (1 if end_pos.row > start_pos.row else -1)
        step_c = 0 if col_diff == 0 else (1 if end_pos.col > start_pos.col else -1)

        row = start_pos.row + step_r
        col = start_pos.col + step_c

        while (row, col) != (end_pos.row, end_pos.col):
            if board.get_piece(Position(row, col)):
                return False

            row += step_r
            col += step_c

        return True
