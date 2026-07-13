from chess_io.board_mapper import BoardMapper
from engine.game_engine import GameEngine


class Controller:

    def __init__(self, board):
        self.board = board
        self.engine = GameEngine(board)
        self.mapper = BoardMapper(board)

    def execute_command(self, command, args):
        if command == "click":
            self._handle_click(args)

        elif command == "wait":
            pass

    def _handle_click(self, args):
        if len(args) != 2:
            return

        try:
            x = int(args[0])
            y = int(args[1])
        except ValueError:
            return

        position = self.mapper.pixel_to_position(x, y)

        if position is None:
            return

        self.engine.handle_click(position)
