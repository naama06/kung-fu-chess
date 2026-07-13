from model.board import Board
from model.position import Position

from model.rook import Rook
from model.king import King


class BoardParser:

    @staticmethod
    def parse(text: str) -> Board:

        lines = text.strip().split('\n')

        board = Board(len(lines[0].split()), len(lines))

        for row_idx, line in enumerate(lines):

            cells = line.split()

            for col_idx, cell in enumerate(cells):

                if cell == '.':
                    continue

                # פורמט ישן: R / r
                if len(cell) == 1:
                    color = "white" if cell.isupper() else "black"
                    piece_type = cell.upper()

                # פורמט חדש: wR / bK
                elif len(cell) == 2:
                    if cell[0] not in ("w", "b"):
                        continue

                    color = "white" if cell[0] == "w" else "black"
                    piece_type = cell[1]

                else:
                    continue

                if piece_type == 'R':
                    piece = Rook(color)

                elif piece_type == 'K':
                    piece = King(color)

                else:
                    continue

                board.add_piece(piece, Position(row_idx, col_idx))

        return board