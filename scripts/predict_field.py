"""Run the wheat / non-wheat classifier over one 6-band GeoTIFF.

Usage:
    python scripts/predict_field.py path/to/plot.tif --out results/

Input must follow the dataset's band order (Blue, Green, Red, RedEdge, NIR,
NDVI), e.g. any file from "Component2-Processed UAV Imagery" of
https://zenodo.org/records/7860751 .

Writes <name>_prob_wheat.npy, <name>_ndvi.npy and <name>_map.png.
"""

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agrofly import load_model, predict_field  # noqa: E402

REPO = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("tif", type=Path)
    parser.add_argument("--weights", type=Path, default=REPO / "models" / "best_model.pth")
    parser.add_argument("--out", type=Path, default=Path("results"))
    parser.add_argument("--threshold", type=float, default=0.5,
                        help="P(wheat) below this counts as non-wheat")
    args = parser.parse_args()

    import rasterio
    import torch
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = load_model(str(args.weights), device)

    with rasterio.open(args.tif) as src:
        image = src.read()
    if image.shape[0] != 6:
        sys.exit(f"Expected 6 bands (B, G, R, RE, NIR, NDVI), got {image.shape[0]}")

    prob, ndvi, valid = predict_field(image, model, device)

    n_valid = int(valid.sum())
    n_non_wheat = int(np.sum(prob[valid] < args.threshold))
    print(f"Grid: {prob.shape[0]} x {prob.shape[1]} tiles, valid: {n_valid}")
    if n_valid:
        print(f"Wheat: {n_valid - n_non_wheat} ({100 * (n_valid - n_non_wheat) / n_valid:.1f}%)  "
              f"Non-wheat: {n_non_wheat} ({100 * n_non_wheat / n_valid:.1f}%)  "
              f"Mean NDVI: {np.nanmean(ndvi):.3f}")

    args.out.mkdir(parents=True, exist_ok=True)
    stem = args.tif.stem
    np.save(args.out / f"{stem}_prob_wheat.npy", prob)
    np.save(args.out / f"{stem}_ndvi.npy", ndvi)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    im0 = axes[0].imshow(prob, cmap="RdYlGn", vmin=0, vmax=1, interpolation="nearest")
    axes[0].set_title("P(wheat) per 64x64 tile")
    fig.colorbar(im0, ax=axes[0], fraction=0.046)
    im1 = axes[1].imshow(ndvi, cmap="RdYlGn", vmin=-0.1, vmax=0.8, interpolation="nearest")
    axes[1].set_title("Mean NDVI per tile")
    fig.colorbar(im1, ax=axes[1], fraction=0.046)
    fig.suptitle(stem)
    fig.tight_layout()
    fig.savefig(args.out / f"{stem}_map.png", dpi=120)
    print(f"Saved to {args.out}/")


if __name__ == "__main__":
    main()
