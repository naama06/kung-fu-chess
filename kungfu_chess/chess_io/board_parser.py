from model.board import Board
from model.position import Position
from model.piece import Piece

class BoardParser:
   @staticmethod
   def parse(text: str) -> Board:
        lines = text.strip().split('\n')
        board = Board(len(lines[0].split()), len(lines))
        
        for row_idx, line in enumerate(lines):
            cells = line.split()
            for col_idx, cell in enumerate(cells):
                if cell == '.':
                    continue # תא ריק, לא עושים כלום
                
                # בדיקה של צבע לפי אותיות (קונבנציה מקובלת)
                color = 'white' if cell.isupper() else 'black'
                piece = Piece(cell.upper(), color)
                board.add_piece(piece, Position(row_idx, col_idx))
        
        return board