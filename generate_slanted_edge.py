
"""
Generate a synthetic slanted-edge image (32-bit/32-bit TIFF) for MTF validation.
Memory-safe streaming version (no huge mgrid allocation).
"""

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from pathlib import Path

# --- Parameters ---
OUTPUT_DIR = Path("point_source_output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH_32 = OUTPUT_DIR / "synthetic_slanted_edge.tiff"
OUTPUT_PATH_16 = OUTPUT_DIR / "synthetic_slanted_edge_16bit.tiff"

PIXEL_PITCH_MM = 0.1
IMAGE_SHAPE = (1600, 1600)   # (rows, cols)
OVERSAMPLE = 32              # oversampling factor
EDGE_ANGLE_DEG = 2.0         # slanted edge angle
EDGE_OFFSET_FRAC = 0.5       # edge position as fraction of width
BLUR_SIGMA_MM = 0.0          # 0 = pixel-aperture-only truth

# --- Derived sizes ---
rows_os = IMAGE_SHAPE[0] * OVERSAMPLE
cols_os = IMAGE_SHAPE[1] * OVERSAMPLE

theta = np.deg2rad(EDGE_ANGLE_DEG).astype(np.float64)
c = float(np.cos(theta))
s = float(np.sin(theta))

x0 = cols_os * EDGE_OFFSET_FRAC

# --- Precompute x term (1D) ---
xx_os = np.arange(cols_os, dtype=np.float32)  # 0..cols_os-1
x_term = xx_os * np.float32(c)                # (cols_os,)

# --- Output image on detector grid ---
out = np.empty(IMAGE_SHAPE, dtype=np.float32)

# --- Stream one detector row at a time ---
for r in range(IMAGE_SHAPE[0]):
    y0 = r * OVERSAMPLE
    yy_os = (y0 + np.arange(OVERSAMPLE, dtype=np.float32))  # (OVERSAMPLE,)

    val = x_term[None, :] + (yy_os[:, None] * np.float32(s))
    block = (val > np.float32(x0)).astype(np.float32)

    block = block.reshape(
        OVERSAMPLE, IMAGE_SHAPE[1], OVERSAMPLE
    ).mean(axis=2)

    out[r, :] = block.mean(axis=0)

# --- Optional blur (mm -> detector pixels) ---
if BLUR_SIGMA_MM > 0:
    sigma_px = (BLUR_SIGMA_MM / PIXEL_PITCH_MM)
    out = gaussian_filter(out, sigma=sigma_px, mode="nearest")

# --- Save 32-bit float TIFF (quantitative reference) ---
Image.fromarray(out.astype(np.float32), mode="F").save(OUTPUT_PATH_32)

# --- Save additional 16-bit TIFF ---
out_min = out.min()
out_max = out.max()
out_16 = ((out - out_min) / (out_max - out_min) * 65535).astype(np.uint16)

Image.fromarray(out_16, mode="I;16").save(OUTPUT_PATH_16)

print(f"Saved: {OUTPUT_PATH_32}")
print(f"Saved: {OUTPUT_PATH_16}")
