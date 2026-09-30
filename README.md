# AgroFly — drone-based crop field analysis

AgroFly is a two-person student project on precision agriculture in Kazakhstan. The idea: a scout drone images a field, a neural network classifies every ~2×2 m tile, and the result is a field map that shows where treatment is needed. The long-term concept adds a second, spraying drone that treats only those tiles instead of the whole field.

This repository holds the software and ML side. Landing page: [agrofly-website-1](https://github.com/Eye172/agrofly-website-1).

**Status: paused while the data and ML approach are being re-evaluated.**

## What exists and what doesn't

| Part | Status |
|---|---|
| Stage 1: grid + NDVI baseline notebook (Feb 2026) | Done; has a band-mapping issue, see notebook header |
| Stage 2: ResNet18 wheat / soybean tile classifier (Jun 2026) | Trained; weights in `models/` |
| Field-map inference code (`src/`, `scripts/`) | Done; tested on a synthetic GeoTIFF |
| Scout drone (RGB + NIR cameras) | Built and flies; no survey mission flown yet |
| Weed / disease detection | **Not done.** No weed imagery was used |
| Sprayer drone | **Concept only.** Not built or purchased |
| Own field imagery, customers, revenue | None |

## Stage 2 model

- **Input:** 64×64 px tiles (~2×2 m) with 6 channels: Blue, Green, Red, RedEdge, NIR, NDVI.
- **Architecture:** ResNet18, ImageNet-pretrained, first conv widened to 6 channels; 11.19 M parameters.
- **Classes:** wheat vs soybean (soybean is labelled "non-wheat" in code).
- **Training data:** 24,000 training tiles and 6,000 validation tiles, 15 epochs on a Tesla T4.
- **Best validation accuracy:** 99.75% (epoch 9).

That number has clear limits:

- The train/val split is random at tile level, so tiles from the same images are on both sides. The result was not tested on an independent field.
- On a wheat plot never used for training (same field and season), 97.0% of tiles were classified as wheat. The other 3.0% are false alarms.
- The "infestation" demo maps are synthetic mosaics built from training-pool tiles, with soybean and barley standing in for weeds.
- The model has no "unknown" class and answers confidently on inputs unlike its training data.

Full numbers and figures: [docs/results.md](docs/results.md).

![training history](docs/img/training_history.png)

## Dataset

**A. Maulit, A. Nugumanova, K. Apayev, Y. Baiburin, M. Sutula.** *A multispectral UAV imagery dataset of wheat, soybean, and barley crops in East Kazakhstan.* Zenodo, 2023.
<https://zenodo.org/records/7860751> — [doi:10.5281/zenodo.7860751](https://doi.org/10.5281/zenodo.7860751), CC BY 4.0.
Paper: *Data* 2023, 8(5), 88 — [doi:10.3390/data8050088](https://doi.org/10.3390/data8050088).

Used file: `Component2-Processed UAV Imagery.zip` (~22 GB). It contains DJI Phantom 4 Multispectral imagery from the 2022 season: 27 one-hectare plots, 5 flights, and 6-band GeoTIFFs. The data is not included in this repo.

## Quick start

```bash
pip install -r requirements.txt
python scripts/predict_field.py "path/to/wheat/13/13_06-08.tif" --out results/
```

This prints the wheat / non-wheat share and writes a P(wheat) map, an NDVI map and a PNG preview. The input must use the dataset's 6-band order.

```python
import sys; sys.path.insert(0, "src")
from agrofly import load_model, predict_field
model = load_model("models/best_model.pth")
prob_wheat, mean_ndvi, valid = predict_field(image, model)  # image: (6, H, W) array
```

## Repository layout

```
notebooks/
  stage1_grid_ndvi.ipynb                  # Feb 2026: grid + NDVI baseline
  stage2_resnet18_wheat_classifier.ipynb  # Jun 2026: data prep, training, maps (Colab, with outputs)
src/agrofly/     # bands, tiling/normalization, model, whole-image inference
scripts/         # predict_field.py CLI
models/          # best_model.pth (state_dict, 45 MB) + model_metadata.json
docs/            # results, hardware, stage 1 notes, figures
```

## Hardware

Two drones are planned. The **scout drone** is built: a 7" quad with a Raspberry Pi Zero 2 W and RGB + NoIR cameras. It flies, but it has not surveyed a field yet. The **sprayer drone** is a concept only. Details, and why the current model cannot be applied to the scout drone's cameras as-is: [docs/hardware.md](docs/hardware.md).

## Business model (concept)

The plan is Agro-as-a-Service: the team flies the field and delivers a treatment map, and the farmer pays per hectare instead of buying a drone. Nothing has been sold, and there are no pilots yet.

## Next steps

1. Split data by plot or date and report held-out accuracy per plot.
2. Get representative data for the real target (weeds, diseases): ask agricultural universities, or fly the scout drone and have an agronomist label the images.
3. Match the sensor to the model: use a multispectral camera, or retrain on RGB + NIR from the team's own drone.
4. Add an "unknown / out-of-distribution" check before any map is shown to a farmer.

## Team

- **Akhmer Shakhnazar** — team lead, software and ML (model, notebooks, website)
- **Bauyrzhan Nurali** — hardware engineer (drone design and build)
