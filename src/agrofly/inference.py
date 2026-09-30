"""Whole-image inference: cut a 6-band image into tiles and score each tile."""

import numpy as np
import torch

from .bands import NDVI, RED
from .tiles import TILE_SIZE, is_valid_tile, normalize_tile


@torch.no_grad()
def predict_field(image: np.ndarray, model: torch.nn.Module,
                  device: str | torch.device = "cpu",
                  tile_size: int = TILE_SIZE, batch_size: int = 256):
    """Score every valid tile of a (6, H, W) image.

    Returns three (rows, cols) arrays:
      prob_wheat - P(wheat) per tile, NaN for skipped tiles
      mean_ndvi  - mean NDVI of the plant pixels in each valid tile, NaN otherwise
      valid      - bool mask of tiles that passed `is_valid_tile`

    The notebook's inference cell skipped the saturation check; here the
    exact training filter is used, so a few saturated tiles may differ.
    """
    _, h, w = image.shape
    n_rows, n_cols = h // tile_size, w // tile_size

    prob_wheat = np.full((n_rows, n_cols), np.nan)
    mean_ndvi = np.full((n_rows, n_cols), np.nan)
    valid = np.zeros((n_rows, n_cols), dtype=bool)

    batch, coords = [], []

    def flush():
        x = torch.from_numpy(np.stack(batch)).to(device)
        probs = torch.softmax(model(x), dim=1)[:, 1].cpu().numpy()
        for (r, c), p in zip(coords, probs):
            prob_wheat[r, c] = p
        batch.clear()
        coords.clear()

    for r in range(n_rows):
        for c in range(n_cols):
            tile = image[:, r * tile_size:(r + 1) * tile_size,
                         c * tile_size:(c + 1) * tile_size]
            if not is_valid_tile(tile):
                continue
            valid[r, c] = True
            mean_ndvi[r, c] = tile[NDVI][tile[RED] > 0].mean()
            batch.append(normalize_tile(tile))
            coords.append((r, c))
            if len(batch) == batch_size:
                flush()

    if batch:
        flush()

    return prob_wheat, mean_ndvi, valid
