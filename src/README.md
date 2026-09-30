# src/agrofly

Code extracted from the Stage 2 notebook so the model runs outside Colab.

- `bands.py`: band order of the dataset, NDVI
- `tiles.py`: 64×64 tiling, tile filter, normalization, grid names (A1, B4, …)
- `model.py`: 6-channel ResNet18, loading `models/best_model.pth`
- `inference.py`: `predict_field()` scores a whole (6, H, W) image tile by tile
