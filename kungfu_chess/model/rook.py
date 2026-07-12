from model.board import Board
from model.piece import Piece
from model.position import Position

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color=color, piece_type='rook')

    @property
    def symbol(self):
        return 'R'

    def is_valid_move(self, board, start_pos, end_pos):
        row_diff = abs(start_pos.row - end_pos.row)
        col_diff = abs(start_pos.col - end_pos.col)
        # צריח זז רק בקו ישר (שורה או עמודה)
        is_straight = (row_diff == 0 and col_diff > 0) or (col_diff == 0 and row_diff > 0)
        return is_straight

    def get_possible_moves(self, board, position):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in directions:
            current_r, current_c = position.row + dr, position.col + dc
            while 0 <= current_r < board.height and 0 <= current_c < board.width:
                target_pos = Position(current_r, current_c)
                piece_at_target = board.get_piece(target_pos)
                if piece_at_target is None:
                    moves.append(target_pos)
                else:
                    if piece_at_target.color != self.color:
                        moves.append(target_pos)
                    break
                current_r += dr
                current_c += dc
        return moves