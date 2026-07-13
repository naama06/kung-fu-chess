from model.piece import Piece


class Knight(Piece):

    def __init__(self,color):
        super().__init__(piece_type='knight',color=color)


    @property
    def symbol(self):
        return 'N'


    def is_valid_move(self,board,start_pos,end_pos):

        row_diff = abs(start_pos.row-end_pos.row)
        col_diff = abs(start_pos.col-end_pos.col)

        return (
            (row_diff == 2 and col_diff == 1)
            or
            (row_diff == 1 and col_diff == 2)
        )