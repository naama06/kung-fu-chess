class GameEngine:
    def __init__(self, board):
        self.board = board
        self.first_click = None

    def handle_click(self, position):
        if self.first_click is None:
            # לחיצה ראשונה: שומרים את מיקום הכלי שנבחר
            piece = self.board.get_piece(position)
            if piece:
                self.first_click = position
        else:
            # לחיצה שנייה: מנסים להזיז את הכלי
            start_pos = self.first_click
            piece = self.board.get_piece(start_pos)
            
            if piece and piece.is_valid_move(self.board, start_pos, position):
                self.board.move_piece(start_pos, position)
            
            # מאפסים את הבחירה
            self.first_click = None