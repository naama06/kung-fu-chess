from model.piece import Piece


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

        # צעד קדימה אחד — רק למשבצת ריקה
        if col_diff == 0 and row_diff == direction:
            return target is None

        # אכילה באלכסון קדימה — רק אם יש יריב
        if abs(col_diff) == 1 and row_diff == direction:
            return target is not None and target.color != self.color

        return False
