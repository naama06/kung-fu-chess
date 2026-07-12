from chess_io.board_parser import BoardParser
from model.position import Position

def test_parse_simple_board():
    # 1. טקסט של לוח עם צריח לבן וצריח שחור
    board_text = "R .\n. r"
    
    # 2. הרצת ה-Parser
    board = BoardParser.parse(board_text)
    
    # 3. בדיקות (Assertions)
    # האם הלוח בגודל 2 על 2?
    assert board.width == 2
    assert board.height == 2
    
    # האם הצריח הלבן נמצא ב-(0,0)?
    piece1 = board.get_piece(Position(0, 0))
    assert piece1.piece_type == 'R'
    assert piece1.color == 'white'
    
    # האם הצריח השחור נמצא ב-(1,1)?
    piece2 = board.get_piece(Position(1, 1))
    assert piece2.piece_type == 'R'
    assert piece2.color == 'black'
    
    print("Test passed!")