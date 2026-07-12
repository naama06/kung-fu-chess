from model.board import Board
from model.position import Position

class BoardParser:
    @staticmethod
    def parse(text: str) -> Board:
        lines = text.strip().split('\n')
        # כאן נחשב את הגודל ונציב את הכלים בלוח
        board = Board(len(lines[0].split()), len(lines))
        # בהמשך נוסיף כאן לוגיקה שתעבור שורה-שורה ותוסיף כלים ללוח
        return board