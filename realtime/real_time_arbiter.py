from model.position import Position
from realtime.motion import Motion


MS_PER_CELL = 1000


class RealTimeArbiter:

    def __init__(self, board):
        self.board = board
        self.active_motions = []

    def can_start_motion(self, start, end):
        piece = self.board.get_piece(start)

        if piece is None:
            return False

        for motion in self.active_motions:
            if motion.color == piece.color:
                return False

            if self._has_common_route(
                motion.start,
                motion.end,
                start,
                end,
            ):
                return False

        return True

    def start_motion(self, start, end):
        if not self.can_start_motion(start, end):
            return

        piece = self.board.get_piece(start)
        distance = self._travel_distance(start, end, piece)
        duration_ms = distance * MS_PER_CELL

        self.active_motions.append(
            Motion(start, end, duration_ms, piece.color)
        )

    def advance(self, ms):
        if not self.active_motions:
            return

        for motion in self.active_motions:
            motion.elapsed_ms += ms

        completed = [
            motion
            for motion in self.active_motions
            if motion.is_complete()
        ]

        for motion in completed:
            self.board.move_piece(motion.start, motion.end)

        self.active_motions = [
            motion
            for motion in self.active_motions
            if not motion.is_complete()
        ]

    def _travel_distance(self, start, end, piece):
        row_diff = abs(end.row - start.row)
        col_diff = abs(end.col - start.col)

        if piece.piece_type == "knight":
            return row_diff + col_diff

        return max(row_diff, col_diff)

    def _has_common_route(self, start1, end1, start2, end2):
        cells1 = self._path_cells(start1, end1)
        cells2 = self._path_cells(start2, end2)

        if cells1 & cells2:
            return True

        if (
            start1.row == end1.row
            and start2.row == end2.row
            and start1.row != start2.row
            and self._column_range(start1, end1)
            & self._column_range(start2, end2)
        ):
            return True

        if (
            start1.col == end1.col
            and start2.col == end2.col
            and start1.col != start2.col
            and self._row_range(start1, end1)
            & self._row_range(start2, end2)
        ):
            return True

        return False

    def _path_cells(self, start, end):
        cells = set()

        if start.row == end.row:
            for col in self._column_range(start, end):
                cells.add(Position(start.row, col))

        elif start.col == end.col:
            for row in self._row_range(start, end):
                cells.add(Position(row, start.col))

        elif abs(end.row - start.row) == abs(end.col - start.col):
            row_step = 1 if end.row > start.row else -1
            col_step = 1 if end.col > start.col else -1

            row = start.row
            col = start.col

            while True:
                cells.add(Position(row, col))

                if row == end.row and col == end.col:
                    break

                row += row_step
                col += col_step

        else:
            cells.add(start)
            cells.add(end)

        return cells

    def _column_range(self, start, end):
        low = min(start.col, end.col)
        high = max(start.col, end.col)
        return set(range(low, high + 1))

    def _row_range(self, start, end):
        low = min(start.row, end.row)
        high = max(start.row, end.row)
        return set(range(low, high + 1))
