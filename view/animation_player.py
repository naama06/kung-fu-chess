class AnimationPlayer:

    def __init__(self, frame_count: int, fps: float, loop: bool = True):
        self.frame_count = max(frame_count, 1)
        self.frame_duration_ms = 1000.0 / max(fps, 1)
        self.loop = loop
        self.elapsed_ms = 0

    def tick(self, ms: int):
        self.elapsed_ms += ms

    def current_index(self) -> int:
        index = int(self.elapsed_ms / self.frame_duration_ms)

        if self.loop:
            return index % self.frame_count

        return min(index, self.frame_count - 1)
