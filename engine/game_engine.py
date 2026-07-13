from engine.rule_engine import RuleEngine


class GameEngine:

    def __init__(self, board):
        self.board = board
        self.rule_engine = RuleEngine()
        self.first_click = None

    def handle_click(self, position):
        if self.first_click is None:
            self._select_piece(position)
            return

        start = self.first_click
        selected = self.board.get_piece(start)

        if selected and self._is_same_color_reselect(selected, position):
            self.first_click = position
            return

        self.request_move(start, position)
        self.first_click = None

    def request_move(self, start, end):
        if not self.rule_engine.is_move_allowed(self.board, start, end):
            return

        self.board.move_piece(start, end)

    def _select_piece(self, position):
        piece = self.board.get_piece(position)

        if piece:
            self.first_click = position

    def _is_same_color_reselect(self, selected_piece, position) -> bool:
        clicked = self.board.get_piece(position)

        return (
            clicked is not None
            and clicked.color == selected_piece.color
        )
