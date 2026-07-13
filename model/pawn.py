from model.piece import Piece


class Pawn(Piece):

    def __init__(self, color):
        super().__init__(piece_type="pawn", color=color)

    @property
    def symbol(self):
        return "P"

    def is_valid_move(self, board, start_pos, end_pos):
        return False
