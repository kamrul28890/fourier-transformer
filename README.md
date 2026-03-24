# Fourier Image Traits Project

This project does two things:

1. Computes and visualizes the Fourier transform of a single image.
2. Downloads a photo dataset from online (Wikimedia Commons), computes Fourier features for all images, and identifies spectral patterns/traits using clustering.

## What you get

- Single-image Fourier spectrum visualization.
- Bulk FFT feature extraction across a dataset.
- Pattern discovery with PCA + KMeans clustering.
- Outputs for analysis and identification traits:
  - `fft_features.csv`
  - `cluster_summary.csv`
  - `analysis_summary.json`
  - `cluster_scatter.png`

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

### 1) Fourier transform for one image

```bash
PYTHONPATH=src python -m fourier_traits.cli single \
  --image path/to/your_image.jpg \
  --out-dir outputs/single
```

Output image:
- `outputs/single/single_fft_only.png`
- `outputs/single/single_fft_side_by_side.png`

### 1b) Fourier transform for all images in a folder

```bash
PYTHONPATH=src python -m fourier_traits.cli transform-all \
  --images-dir data/images \
  --out-dir outputs/all_transforms
```

Batch outputs:
- `outputs/all_transforms/fft_only/`
- `outputs/all_transforms/side_by_side/`
- `outputs/all_transforms/transform_manifest.json`

### 1c) Annotated side-by-side for all images (with explanation text)

```bash
PYTHONPATH=src python -m fourier_traits.cli explain-all \
  --images-dir data/images \
  --out-dir outputs/explained_transforms
```

Annotated outputs:
- `outputs/explained_transforms/annotated_side_by_side/`
- `outputs/explained_transforms/fft_reasoning_table.csv`

### 2) Download online image dataset

Wikimedia source (query-based):

```bash
PYTHONPATH=src python -m fourier_traits.cli fetch \
  --source wikimedia \
  --query "street photography" \
  --limit 150 \
  --out-dir data/images
```

Picsum source (random photos, usually better for larger batches):

```bash
PYTHONPATH=src python -m fourier_traits.cli fetch \
  --source picsum \
  --limit 150 \
  --size 512 \
  --out-dir data/images
```

### 3) Run FFT pattern and trait analysis

```bash
PYTHONPATH=src python -m fourier_traits.cli analyze \
  --images-dir data/images \
  --out-dir outputs/analysis \
  --bins 64 \
  --clusters 6
```

## How trait identification works

Each image is converted to grayscale, resized, transformed to frequency domain, and represented by:

- Radial power profile bins (energy distribution from low to high frequencies).
- Frequency-band energy ratios (low/mid/high).
- Spectral centroid (where energy is concentrated).
- Anisotropy score (directional structure in frequency content).

The project then scales these features and groups images via KMeans. Cluster-level averages in `cluster_summary.csv` can be interpreted as identification traits.

## Notes

- Online download uses public Wikimedia API and does not require an API key.
- Downloads depend on network availability and source content quality.
- For stronger trait identification, try larger datasets and domain-specific queries (e.g., faces, leaves, roads, radiology scans).
