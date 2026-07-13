class Motion:

    def __init__(self, start, end, duration_ms):
        self.start = start
        self.end = end
        self.duration_ms = duration_ms
        self.elapsed_ms = 0

    def is_complete(self):
        return self.elapsed_ms >= self.duration_ms
