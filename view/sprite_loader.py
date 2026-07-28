import json
from pathlib import Path

import cv2
import numpy as np

from graphics.img import Img
from view.assets_config import (
    PIECE_CROP_BOTTOM_RATIO,
    PIECES_DIR,
    STATIC_ANIM_STATES,
)
from view.piece_assets import piece_folder_name


class SpriteLoader:

    def __init__(self, pieces_root: Path | None = None):
        self.pieces_root = pieces_root or PIECES_DIR
        self._cache: dict[tuple[str, str], list[Img]] = {}
        self._meta: dict[tuple[str, str], dict] = {}

    def get_animation_meta(self, color: str, piece_type: str, state: str) -> dict:
        key = (piece_folder_name(color, piece_type), state)
        if key not in self._meta:
            config_path = (
                self.pieces_root / key[0] / "states" / state / "config.json"
            )
            with open(config_path, encoding="utf-8") as file:
                self._meta[key] = json.load(file)

        return self._meta[key]

    def get_frames(
        self,
        color: str,
        piece_type: str,
        state: str,
        size: tuple[int, int],
    ) -> list[Img]:
        key = (piece_folder_name(color, piece_type), state)

        if key not in self._cache:
            sprites_dir = self.pieces_root / key[0] / "states" / state / "sprites"
            sprite_paths = sorted(
                sprites_dir.glob("*.png"),
                key=lambda path: int(path.stem),
            )

            if state in STATIC_ANIM_STATES:
                sprite_paths = sprite_paths[:1]

            frames = [
                self._load_clean_frame(sprite_path, size)
                for sprite_path in sprite_paths
            ]
            self._cache[key] = frames

        return self._cache[key]

    def _load_clean_frame(self, sprite_path: Path, size: tuple[int, int]) -> Img:
        raw = cv2.imread(str(sprite_path), cv2.IMREAD_UNCHANGED)

        if raw is None:
            raise FileNotFoundError(f"Cannot load sprite: {sprite_path}")

        cleaned = self._crop_debug_footer(raw)
        cleaned = self._remove_debug_text(cleaned)

        frame = Img()
        frame.img = cv2.resize(
            cleaned,
            size,
            interpolation=cv2.INTER_AREA,
        )
        return frame

    def _crop_debug_footer(self, image: np.ndarray) -> np.ndarray:
        crop_rows = int(image.shape[0] * PIECE_CROP_BOTTOM_RATIO)

        if crop_rows <= 0:
            return image

        return image[: image.shape[0] - crop_rows, :]

    def _remove_debug_text(self, image: np.ndarray) -> np.ndarray:
        if image.ndim == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        has_alpha = image.shape[2] == 4
        bgr = image[:, :, :3].copy()
        alpha = image[:, :, 3].copy() if has_alpha else None

        b = bgr[:, :, 0].astype(np.int16)
        g = bgr[:, :, 1].astype(np.int16)
        r = bgr[:, :, 2].astype(np.int16)

        debug_mask = (
            ((b > 140) & (g < 140) & (r < 140))
            | ((g > 110) & (b < 120) & (r < 120))
        ).astype(np.uint8) * 255

        if np.any(debug_mask):
            bgr = cv2.inpaint(bgr, debug_mask, 5, cv2.INPAINT_TELEA)

        if has_alpha:
            return cv2.merge([bgr[:, :, 0], bgr[:, :, 1], bgr[:, :, 2], alpha])

        return cv2.cvtColor(bgr, cv2.COLOR_BGR2BGRA)
