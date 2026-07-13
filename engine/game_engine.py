from engine.rule_engine import RuleEngine
from model.game_state import GameState
from realtime.real_time_arbiter import RealTimeArbiter


class GameEngine:

    def __init__(self, board):
        self.board = board
        self.rule_engine = RuleEngine()
        self.arbiter = RealTimeArbiter(board)
        self.game_state = GameState()
        self.first_click = None
        self.premove = None

    def handle_click(self, position):
        if self.game_state.is_game_over():
            return

        if self.first_click is None:
            self._select_piece(position)
            return

        start = self.first_click
        selected = self.board.get_piece(start)

        if selected and self._is_same_color_reselect(selected, position):
            self.first_click = position
            return

        if self.arbiter.is_piece_moving(start):
            motion = self.arbiter.get_motion_at(start)
            self.premove = (motion.start, motion.end, position)
            self.first_click = None
            return

        self.request_move(start, position)
        self.first_click = None

    def request_move(self, start, end):
        if self.game_state.is_game_over():
            return

        if not self.rule_engine.is_move_allowed(self.board, start, end):
            return

        self.arbiter.start_motion(start, end)

    def handle_jump(self, position):
        if self.game_state.is_game_over():
            return

        self.arbiter.start_jump(position)

    def advance_time(self, ms):
        captured_pieces = self.arbiter.advance(ms)
        self._check_king_captures(captured_pieces)

        if self.game_state.is_game_over():
            self.premove = None
            self.first_click = None
            return

        self._try_execute_premove()

    def _check_king_captures(self, captured_pieces):
        for piece in captured_pieces:
            if piece.piece_type == "king":
                self.game_state.mark_game_over()

    def _try_execute_premove(self):
        if self.premove is None:
            return

        motion_start, motion_end, destination = self.premove

        if self.arbiter.is_piece_moving(motion_start):
            return

        self.premove = None

        if self.arbiter.has_common_route(
            motion_start,
            motion_end,
            motion_end,
            destination,
        ):
            return

        if not self.rule_engine.is_move_allowed(
            self.board,
            motion_end,
            destination,
        ):
            return

        self.arbiter.start_motion(motion_end, destination)

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
