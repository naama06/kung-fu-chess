import json
from typing import Any

from view.game_snapshot import GameSnapshot, PieceView


def piece_from_dict(data: dict[str, Any]) -> PieceView:
    return PieceView(
        color=data["color"],
        piece_type=data["piece_type"],
        row=data["row"],
        col=data["col"],
        anim_state=data["anim_state"],
        is_selected=data.get("is_selected", False),
    )


def snapshot_from_dict(data: dict[str, Any]) -> GameSnapshot:
    return GameSnapshot(
        board_width=data["board_width"],
        board_height=data["board_height"],
        pieces=[piece_from_dict(piece) for piece in data.get("pieces", [])],
        game_over=data.get("game_over", False),
        white_score=data.get("white_score", 0),
        black_score=data.get("black_score", 0),
        white_name=data.get("white_name", "White"),
        black_name=data.get("black_name", "Black"),
        white_moves=data.get("white_moves", []),
        black_moves=data.get("black_moves", []),
    )


def piece_to_dict(piece: PieceView) -> dict[str, Any]:
    return {
        "color": piece.color,
        "piece_type": piece.piece_type,
        "row": piece.row,
        "col": piece.col,
        "anim_state": piece.anim_state,
        "is_selected": piece.is_selected,
    }


def snapshot_to_dict(snapshot: GameSnapshot) -> dict[str, Any]:
    return {
        "board_width": snapshot.board_width,
        "board_height": snapshot.board_height,
        "pieces": [piece_to_dict(piece) for piece in snapshot.pieces],
        "game_over": snapshot.game_over,
        "white_score": snapshot.white_score,
        "black_score": snapshot.black_score,
        "white_name": snapshot.white_name,
        "black_name": snapshot.black_name,
        "white_moves": snapshot.white_moves,
        "black_moves": snapshot.black_moves,
    }


def encode_message(message: dict[str, Any]) -> str:
    return json.dumps(message, ensure_ascii=False)


def decode_message(text: str) -> dict[str, Any]:
    return json.loads(text)
