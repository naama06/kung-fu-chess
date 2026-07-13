class AirborneJump:

    DURATION_MS = 1000

    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.elapsed_ms = 0

    def is_complete(self):
        return self.elapsed_ms >= self.DURATION_MS
