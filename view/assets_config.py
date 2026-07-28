from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
BOARD_IMAGE = ASSETS_DIR / "board.png"

PIECES_DIR = PROJECT_ROOT / "_ctd26_repo" / "pieces1"
if not PIECES_DIR.exists():
    PIECES_DIR = PROJECT_ROOT / "_ctd26_repo" / "pieces2"
if not PIECES_DIR.exists():
    PIECES_DIR = PROJECT_ROOT / "assets" / "pieces1"

PIECE_CROP_BOTTOM_RATIO = 0.22
STATIC_ANIM_STATES = {"idle", "short_rest", "long_rest"}

SIDE_PANEL_WIDTH = 280
TOP_TITLE_HEIGHT = 52
BOARD_PADDING = 24
TARGET_CELL_SIZE = 72
