# Synthetic Slanted-Edge Image Generator

## Description
This script generates a **synthetic slanted-edge image** for **MTF (Modulation Transfer Function) validation** in radiographic imaging systems.

The slanted edge is analytically defined on an **oversampled grid** and then binned to detector resolution, providing accurate pixel-aperture integration while avoiding large memory allocations. The output is a **32-bit floating-point TIFF** and **16-bit floating-point TIFF** suitable for standard slanted-edge MTF analysis pipelines.

---

## Features
- Memory-safe streaming implementation (no large grid allocations)
- Arbitrary slanted-edge angle
- Exact pixel-aperture integration via oversampling
- Optional Gaussian blur defined in physical units (mm)
- Cross-platform compatibility (Windows, Linux, macOS)

---

## Requirements
- Python ≥ 3.8
- Required Python packages:
  - `numpy`
  - `scipy`
  - `Pillow`

Install dependencies:
```bash
pip install numpy scipy pillow
```

---

## Usage
Run the script from the directory containing the file:
```bash
python generate_slanted_edge.py
```

---

## Output
The script creates the following file:
```
point_source_output/synthetic_slanted_edge.tiff
```

- File format: TIFF  
- Data type: 32-bit floating point  
- Pixel values: normalized in the range [0, 1]

The output directory is created automatically if it does not already exist.

---

## Key Parameters (editable in script)
```python
IMAGE_SHAPE = (1600, 1600)   # Detector image size (rows, cols)
PIXEL_PITCH_MM = 0.1        # Detector pixel size in mm
OVERSAMPLE = 32             # Oversampling factor
EDGE_ANGLE_DEG = 2.0        # Slanted-edge angle in degrees
EDGE_OFFSET_FRAC = 0.5      # Edge position as fraction of image width
BLUR_SIGMA_MM = 0.0         # Optional Gaussian blur (mm)
```

Notes:
- Increasing `OVERSAMPLE` improves pixel-aperture accuracy at the cost of computation time.
- Setting `BLUR_SIGMA_MM = 0.0` produces a ground-truth edge limited only by pixel integration.

---

## Method Summary
1. Define a binary Heaviside edge on an oversampled grid.
2. Stream oversampled rows to avoid excessive memory usage.
3. Bin oversampled pixels to detector resolution.
4. Optionally apply Gaussian blur in physical units.
5. Save the result as a floating-point TIFF image.

---

## Intended Use
- Validation of slanted-edge MTF pipelines
- Reference image generation
- Algorithm benchmarking
- Simulation and analysis consistency checks

---

## License
Research use. Cite appropriately if used in academic publications.
