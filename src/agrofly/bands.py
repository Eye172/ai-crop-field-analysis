"""Band layout of the East Kazakhstan multispectral UAV dataset.

Each processed GeoTIFF has 6 bands in this order (0-based index):
0 Blue, 1 Green, 2 Red, 3 RedEdge, 4 NIR, 5 NDVI (precomputed, -1..1).
Bands 0-4 are uint16 reflectance-like values (0..65535).

Dataset: https://zenodo.org/records/7860751 (DOI 10.5281/zenodo.7860751)
"""

import numpy as np

BANDS = ("Blue", "Green", "Red", "RedEdge", "NIR", "NDVI")
BLUE, GREEN, RED, RED_EDGE, NIR, NDVI = range(6)


def compute_ndvi(image: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    """NDVI = (NIR - Red) / (NIR + Red) for a (6, H, W) or (5, H, W) array.

    The Stage 1 notebook hard-coded band 0 as Red and band 3 as NIR (a 4-band
    RGBN layout); for this dataset those are Blue and RedEdge. Use the
    indices above.
    """
    red = image[RED].astype(np.float64)
    nir = image[NIR].astype(np.float64)
    return (nir - red) / (nir + red + eps)
