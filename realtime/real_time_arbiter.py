from realtime.motion import Motion


MS_PER_CELL = 1000


class RealTimeArbiter:

    def __init__(self, board):
        self.board = board
        self.active_motion = None

    def has_active_motion(self):
        return self.active_motion is not None

    def start_motion(self, start, end):
        if self.has_active_motion():
            return

        distance = self._travel_distance(start, end)
        duration_ms = distance * MS_PER_CELL

        self.active_motion = Motion(start, end, duration_ms)

    def _travel_distance(self, start, end):
        piece = self.board.get_piece(start)
        row_diff = abs(end.row - start.row)
        col_diff = abs(end.col - start.col)

        if piece.piece_type == "knight":
            return row_diff + col_diff

        return max(row_diff, col_diff)

    def advance(self, ms):
        if self.active_motion is None:
            return

        self.active_motion.elapsed_ms += ms

        if self.active_motion.is_complete():
            motion = self.active_motion
            self.board.move_piece(motion.start, motion.end)
            self.active_motion = None
