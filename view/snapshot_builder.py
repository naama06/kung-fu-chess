from model.position import Position

from view.game_snapshot import GameSnapshot, PieceView
from view.game_stats import GameStats


class SnapshotBuilder:

    def __init__(self, controller, stats: GameStats):
        self.controller = controller
        self.stats = stats

    def build(self) -> GameSnapshot:
        engine = self.controller.engine
        board = self.controller.board
        arbiter = engine.arbiter
        moving_starts = {
            motion.start for motion in arbiter.active_motions
        }

        pieces: list[PieceView] = []

        for motion in arbiter.active_motions:
            piece = board.get_piece(motion.start)

            if piece is None:
                continue

            progress = min(1.0, motion.elapsed_ms / motion.duration_ms)
            row = motion.start.row + (motion.end.row - motion.start.row) * progress
            col = motion.start.col + (motion.end.col - motion.start.col) * progress

            pieces.append(
                PieceView(
                    color=piece.color,
                    piece_type=piece.piece_type,
                    row=row,
                    col=col,
                    anim_state="move",
                    is_selected=False,
                )
            )

        for row in range(board.height):
            for col in range(board.width):
                position = Position(row, col)
                piece = board.get_piece(position)

                if piece is None:
                    continue

                if position in moving_starts:
                    continue

                anim_state = "idle"

                if (
                    arbiter.airborne_jump is not None
                    and arbiter.airborne_jump.position == position
                    and not arbiter.airborne_jump.is_complete()
                ):
                    anim_state = "jump"

                is_selected = engine.first_click == position

                pieces.append(
                    PieceView(
                        color=piece.color,
                        piece_type=piece.piece_type,
                        row=row,
                        col=col,
                        anim_state=anim_state,
                        is_selected=is_selected,
                    )
                )

        return GameSnapshot(
            board_width=board.width,
            board_height=board.height,
            pieces=pieces,
            game_over=engine.game_state.is_game_over(),
            white_score=self.stats.white_score,
            black_score=self.stats.black_score,
            white_name=self.stats.white_name,
            black_name=self.stats.black_name,
            white_moves=self.stats.white_moves[-12:],
            black_moves=self.stats.black_moves[-12:],
        )
