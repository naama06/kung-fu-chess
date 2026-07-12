from model.board import Board
from model.position import Position
from model.rook import Rook

def test_rook_moves():
    # 1. יצירת לוח (הלוח הוא תשתית בלבד)
    board = Board(8, 8)
    
    # 2. הצבת צריח לבן במיקום נתון
    rook = Rook(color='white')
    pos = Position(4, 4)
    board.add_piece(rook, pos)
    
    # 3. הפעלת הלוגיקה של הצריח (הצריח מחליט לאן לזוז לפי הלוח)
    moves = rook.get_possible_moves(board, pos)
    
    # 4. בדיקת התנהגות (האם הוא יודע לזוז ישר לכל הכיוונים?)
    # 14 משבצות אפשריות בקו ישר (8 בשורה + 8 בעמודה פחות המקום שלו)
    assert len(moves) == 14
    assert Position(4, 5) in moves  # ימינה
    assert Position(4, 3) in moves  # שמאלה
    assert Position(5, 4) in moves  # למטה
    assert Position(3, 4) in moves  # למעלה
    
    print("Test passed: Rook movement logic is correct.")