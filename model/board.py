from model.position import Position


class Board:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._pieces = {}   # Position -> Piece


    def add_piece(self, piece, pos):
        self._pieces[pos] = piece


    def get_piece(self, pos):
        return self._pieces.get(pos)


    def remove_piece(self, pos):
        self._pieces.pop(pos, None)

    def move_piece(self, start_pos, end_pos):
        captured = self._pieces.get(end_pos)
        piece = self._pieces.pop(start_pos, None)

        if piece:
            self._pieces[end_pos] = piece

        return captured


    def __str__(self):

        rows = []

        for r in range(self.height):

            row = []

            for c in range(self.width):

                piece = self.get_piece(Position(r, c))

                if piece is None:
                    row.append(".")

                else:
                    color = "w" if piece.color == "white" else "b"

                    row.append(
                        color + piece.symbol
                    )

            rows.append(" ".join(row))

        return "\n".join(rows)