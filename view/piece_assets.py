PIECE_LETTERS = {
    "king": "K",
    "queen": "Q",
    "rook": "R",
    "bishop": "B",
    "knight": "N",
    "pawn": "P",
}

PIECE_VALUES = {
    "pawn": 1,
    "knight": 3,
    "bishop": 3,
    "rook": 5,
    "queen": 9,
}


def piece_folder_name(color: str, piece_type: str) -> str:
    letter = PIECE_LETTERS[piece_type]
    suffix = "W" if color == "white" else "B"
    return f"{letter}{suffix}"


def square_label(col: int, row: int) -> str:
    return f"{chr(ord('a') + col)}{row + 1}"
