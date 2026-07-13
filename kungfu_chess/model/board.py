from model.position import Position

class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._pieces = {} # מיפוי של Position לכלי

    def add_piece(self, piece, pos):
        self._pieces[pos] = piece

    def get_piece(self, pos):
        return self._pieces.get(pos)

    def move_piece(self, start_pos, end_pos):
        # מוציא את הכלי מהמקום הישן ושם אותו בחדש
        piece = self._pieces.pop(start_pos, None)
        if piece:
            self._pieces[end_pos] = piece