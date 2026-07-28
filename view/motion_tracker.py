class MotionTracker:

    def __init__(self):
        self._pending: dict[int, dict] = {}

    def before_advance(self, engine):
        self._pending = {}

        for motion in engine.arbiter.active_motions:
            piece = engine.board.get_piece(motion.start)

            if piece is None:
                continue

            target = engine.board.get_piece(motion.end)

            self._pending[id(motion)] = {
                "motion": motion,
                "color": motion.color,
                "piece_type": piece.piece_type,
                "end": motion.end,
                "target": target,
            }

    def after_advance(self, engine, stats):
        active_ids = {id(motion) for motion in engine.arbiter.active_motions}

        for motion_id, info in self._pending.items():
            if motion_id in active_ids:
                continue

            motion = info["motion"]

            if not motion.is_complete():
                continue

            target = info["target"]
            captured = (
                target is not None
                and target.color != info["color"]
            )

            if captured:
                stats.record_capture(info["color"], target.piece_type)

            stats.record_move(
                info["color"],
                info["piece_type"],
                info["end"].col,
                info["end"].row,
                captured,
            )
