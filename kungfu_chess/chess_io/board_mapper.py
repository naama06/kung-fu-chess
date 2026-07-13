from model.position import Position


CELL_SIZE = 100


class BoardMapper:

    def __init__(self, board):
        self.board = board

    def pixel_to_position(self, x: int, y: int):
        col = x // CELL_SIZE
        row = y // CELL_SIZE

        if not self._is_on_board(row, col):
            return None

        return Position(row, col)

    def _is_on_board(self, row: int, col: int) -> bool:
        return (
            0 <= row < self.board.height
            and 0 <= col < self.board.width
        )
