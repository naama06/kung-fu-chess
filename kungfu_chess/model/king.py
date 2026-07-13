from model.board import Board
from model.piece import Piece
from model.position import Position

class King(Piece):
    def __init__(self, color):
        super().__init__(color=color, piece_type='king')

    @property
    def symbol(self):
        return 'K'

    def is_valid_move(self, board, start_pos, end_pos):
        # אסור להישאר באותו מקום
        if start_pos == end_pos:
            return False
            
        row_diff = abs(start_pos.row - end_pos.row)
        col_diff = abs(start_pos.col - end_pos.col)
        
        # המלך זז רק אם המרחק הוא מקסימום 1 בכל כיוון
        return row_diff <= 1 and col_diff <= 1