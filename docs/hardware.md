# Hardware

The concept uses **two drones**: a scout drone that images the field, and a sprayer drone that treats only the flagged tiles. Only the scout drone exists.

## 1. Scout drone: built, flies

Designed and assembled by the team's hardware engineer (Bauyrzhan Nurali).

![scout drone build](img/scout-drone-build.jpg)

| Part | Component |
|---|---|
| Frame | Mark4 7" (295 mm) |
| Motors | 4 × FlashHobby Arthur A2807 1300KV |
| Flight controller | Fortune F405 V3 + 50 A ESC (STM32F405) |
| Battery | 6S 3200 mAh LiPo |
| Radio | RadioMaster RP3 ELRS 2.4 GHz receiver, RadioMaster Pocket transmitter |
| GPS | M10N GPS + compass |
| Onboard computer | Raspberry Pi Zero 2 W |
| Cameras | RGB camera (IMX179, 8 MP, USB) + near-infrared camera (Raspberry Pi NoIR, IR filter removed) |
| Props | HQProp 7040×3 |

Planned flight mode: an INAV waypoint mission. The field is outlined on a laptop, a serpentine ("snake") route is generated, and the drone flies it autonomously, returning home on low battery. Images are processed on the ground (laptop), not onboard.

**Status:** the drone is assembled and flies. It has **not** yet flown a survey mission over a field, and no imagery from it has been collected or used for training.

**Sensor gap:** the model in this repo was trained on a calibrated 5-band multispectral camera (DJI Phantom 4 Multispectral: Blue, Green, Red, RedEdge, NIR) plus NDVI. An RGB + NoIR pair gives different, uncalibrated bands, so the current model cannot be applied to this drone's images as-is. It needs either a multispectral camera or retraining on the drone's own data.

## 2. Sprayer drone: concept only

Not built and not purchased; a capable spraying platform is expensive. The idea: take the list of flagged tiles from the scout map, plan a route through them, and spray only those spots instead of the whole field.

The team has sketched the parts (membrane pump, MOSFET switch, rotary atomizers), but nothing has been bought, assembled or tested.
