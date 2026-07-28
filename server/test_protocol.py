from server.protocol import snapshot_from_dict, snapshot_to_dict
from view.game_snapshot import GameSnapshot, PieceView


def test_snapshot_roundtrip():
    original = GameSnapshot(
        board_width=8,
        board_height=8,
        pieces=[
            PieceView(
                color="white",
                piece_type="king",
                row=7,
                col=4,
                anim_state="idle",
                is_selected=True,
            )
        ],
        game_over=False,
        white_score=1,
        black_score=0,
        white_name="Alice",
        black_name="Bob",
        white_moves=["  1.0s  Ke1"],
        black_moves=[],
    )

    restored = snapshot_from_dict(snapshot_to_dict(original))

    assert restored.board_width == 8
    assert restored.white_name == "Alice"
    assert len(restored.pieces) == 1
    assert restored.pieces[0].piece_type == "king"
    assert restored.pieces[0].is_selected is True
