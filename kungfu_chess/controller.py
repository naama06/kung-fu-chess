from engine.game_engine import GameEngine
from model.position import Position

class Controller:
    def __init__(self, board):
        self.board = board
        self.engine = GameEngine(board)

    def execute_command(self, command, args):
        if command == "click":
            # הפיכת ה-args למיקום (נניח ש-args זה [row, col])
            pos = Position(int(args[0]), int(args[1]))
            self.engine.handle_click(pos)
        
        elif command == "print":
            if args[0] == "board":
                print(self.board)
                
        elif command == "wait":
            # פקודת wait פשוט לא עושה כלום, היא רק מעכבת את הזמן
            pass