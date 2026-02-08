## Stage 1 Design Notes

- The system processes aerial images of crop fields.
- Images are divided into fixed-size grid sectors.
- Each sector is analyzed independently.
- Results are reconstructed into a unified annotated field map.

## Multispectral TIFF Handling

Some dataset images contain more than three channels (e.g., RGB + NIR).
This caused OpenCV drawing functions to fail during visualization on the program's step5.

The issue was resolved by using only the first three channels for display,
while keeping all channels for analysis.
