class Piece:
    def __init__(self, piece_type: str, color: str):
        self.piece_type = piece_type  # למשל 'R' לצריח
        self.color = color            # למשל 'white' או 'black'

    def __repr__(self):
        return f"{self.color[0].upper()}{self.piece_type}"