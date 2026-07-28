from dataclasses import dataclass, field


@dataclass
class PieceView:
    color: str
    piece_type: str
    row: float
    col: float
    anim_state: str
    is_selected: bool = False


@dataclass
class GameSnapshot:
    board_width: int
    board_height: int
    pieces: list[PieceView] = field(default_factory=list)
    game_over: bool = False
    white_score: int = 0
    black_score: int = 0
    white_name: str = "White"
    black_name: str = "Black"
    white_moves: list[str] = field(default_factory=list)
    black_moves: list[str] = field(default_factory=list)
