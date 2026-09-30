"""AgroFly: tile-based crop classification for multispectral UAV imagery.

Code extracted from notebooks/stage2_resnet18_wheat_classifier.ipynb so the
trained model can be used outside Colab.
"""

from .bands import BANDS, compute_ndvi
from .model import build_model, load_model
from .tiles import TILE_SIZE, is_valid_tile, normalize_tile, tile_name
from .inference import predict_field

__all__ = [
    "BANDS",
    "compute_ndvi",
    "build_model",
    "load_model",
    "TILE_SIZE",
    "is_valid_tile",
    "normalize_tile",
    "tile_name",
    "predict_field",
]
