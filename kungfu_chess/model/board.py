class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._pieces = {} # מיפוי של Position לכלי

    def add_piece(self, piece, pos):
        self._pieces[pos] = piece

    def get_piece(self, pos):
        return self._pieces.get(pos)