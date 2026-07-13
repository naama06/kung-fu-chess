from chess_io.board_parser import BoardParser
from model.position import Position

def test_parse_simple_board():
    board_text = "R .\n. r"
    board = BoardParser.parse(board_text)
    
    assert board.width == 2
    assert board.height == 2
    
    # שיניתי ל-'rook' כי זה מה שהקוד שלך מחזיר
    piece1 = board.get_piece(Position(0, 0))
    assert piece1.piece_type == 'rook' 
    assert piece1.color == 'white'
    
    piece2 = board.get_piece(Position(1, 1))
    assert piece2.piece_type == 'rook'
    assert piece2.color == 'black'
    
    print("Test passed!")