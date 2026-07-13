from model.piece import Piece
from model.position import Position


class Bishop(Piece):

    def __init__(self, color):
        super().__init__(piece_type='bishop', color=color)


    @property
    def symbol(self):
        return 'B'


    def is_valid_move(self, board, start_pos, end_pos):

        if start_pos == end_pos:
            return False

        row_diff = abs(end_pos.row - start_pos.row)
        col_diff = abs(end_pos.col - start_pos.col)

        # רץ חייב אלכסון
        if row_diff != col_diff:
            return False


        step_r = 1 if end_pos.row > start_pos.row else -1
        step_c = 1 if end_pos.col > start_pos.col else -1


        r = start_pos.row + step_r
        c = start_pos.col + step_c


        while (r,c) != (end_pos.row,end_pos.col):

            if board.get_piece(Position(r,c)):
                return False

            r += step_r
            c += step_c


        return True