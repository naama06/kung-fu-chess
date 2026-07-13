class GameEngine:
    def __init__(self, board):
        self.board = board
        self.first_click = None

    def handle_click(self, position):
        if self.first_click is None:
            piece = self.board.get_piece(position)
            if piece:
                self.first_click = position
        else:
            start_pos = self.first_click
            piece = self.board.get_piece(start_pos)
            
            # בדיקה חוקית + בדיקה שהיעד לא תפוס על ידי כלי מאותו צבע
            target_piece = self.board.get_piece(position)
            if piece and piece.is_valid_move(self.board, start_pos, position):
                # בדיקת צבע: אם יש כלי ביעד, הוא חייב להיות בצבע שונה
                if target_piece is None or target_piece.color != piece.color:
                    self.board.move_piece(start_pos, position)
            
            self.first_click = None