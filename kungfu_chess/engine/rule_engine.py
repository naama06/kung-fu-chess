class RuleEngine:

    def is_move_allowed(self, board, start, end) -> bool:
        piece = board.get_piece(start)

        if piece is None:
            return False

        target = board.get_piece(end)

        if target is not None and target.color == piece.color:
            return False

        return piece.is_valid_move(board, start, end)
