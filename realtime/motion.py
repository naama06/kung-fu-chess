class Motion:

    _next_order = 0

    def __init__(self, start, end, duration_ms, color):
        self.start = start
        self.end = end
        self.duration_ms = duration_ms
        self.color = color
        self.elapsed_ms = 0
        self.order = Motion._next_order
        Motion._next_order += 1

    def is_complete(self):
        return self.elapsed_ms >= self.duration_ms

    @classmethod
    def reset_order(cls):
        cls._next_order = 0
