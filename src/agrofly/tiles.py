"""Tiling, filtering and normalization, identical to the training notebook."""

import numpy as np

from .bands import NDVI, RED

TILE_SIZE = 64          # px; ~2 x 2 m at the dataset's ~3 cm GSD
EMPTY_THRESH = 0.3      # drop tile if >30% of Red pixels are 0 (outside the plot)
MIN_NDVI = -0.05        # drop tile if mean NDVI is below this (bare soil / shadow)
SATURATED_THRESH = 0.5  # drop tile if >50% of Red pixels are saturated


def is_valid_tile(tile: np.ndarray) -> bool:
    """Same filter the training tiles went through. `tile` is (6, 64, 64)."""
    red = tile[RED]
    if np.sum(red == 0) / red.size > EMPTY_THRESH:
        return False

    ndvi = tile[NDVI][red > 0]
    if len(ndvi) == 0 or ndvi.mean() < MIN_NDVI:
        return False

    if np.sum(red >= 65530) / red.size > SATURATED_THRESH:
        return False

    return True


def normalize_tile(tile: np.ndarray) -> np.ndarray:
    """Bands 0-4: /65535. NDVI: (x + 1) / 2. Everything clipped to [0, 1]."""
    out = np.zeros_like(tile, dtype=np.float32)
    out[:5] = tile[:5] / 65535.0
    out[5] = (tile[5] + 1.0) / 2.0
    return np.clip(out, 0.0, 1.0)


def col_to_letter(col_idx: int) -> str:
    """0 -> A, 25 -> Z, 26 -> AA (spreadsheet-style column names)."""
    result = ""
    col_idx += 1
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx - 1, 26)
        result = chr(65 + remainder) + result
    return result


def tile_name(row_idx: int, col_idx: int) -> str:
    """Grid label used on field maps, e.g. (0, 1) -> 'B1'."""
    return f"{col_to_letter(col_idx)}{row_idx + 1}"
