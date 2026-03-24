from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


@dataclass
class FourierFeatureSet:
    radial_profile: np.ndarray
    low_energy_ratio: float
    mid_energy_ratio: float
    high_energy_ratio: float
    spectral_centroid: float
    anisotropy: float

    def to_vector(self) -> np.ndarray:
        summary = np.array(
            [
                self.low_energy_ratio,
                self.mid_energy_ratio,
                self.high_energy_ratio,
                self.spectral_centroid,
                self.anisotropy,
            ],
            dtype=np.float32,
        )
        return np.concatenate([self.radial_profile.astype(np.float32), summary])


def load_grayscale_image(image_path: str | Path, size: tuple[int, int] = (256, 256)) -> np.ndarray:
    image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)


def compute_fft_spectrum(image: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    spectrum_complex = np.fft.fftshift(np.fft.fft2(image))
    magnitude = np.abs(spectrum_complex)
    log_magnitude = np.log1p(magnitude)
    return spectrum_complex, log_magnitude


def _radial_profile(power: np.ndarray, bins: int = 64) -> np.ndarray:
    h, w = power.shape
    cy, cx = h // 2, w // 2

    yy, xx = np.indices((h, w))
    radii = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    max_radius = radii.max()

    bin_edges = np.linspace(0.0, max_radius, bins + 1)
    profile = np.zeros(bins, dtype=np.float64)

    for i in range(bins):
        mask = (radii >= bin_edges[i]) & (radii < bin_edges[i + 1])
        if np.any(mask):
            profile[i] = power[mask].mean()

    if profile.sum() > 0:
        profile = profile / profile.sum()

    return profile


def _frequency_band_ratios(power: np.ndarray) -> tuple[float, float, float]:
    h, w = power.shape
    cy, cx = h // 2, w // 2
    yy, xx = np.indices((h, w))
    radii = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    r_max = radii.max()

    low_mask = radii <= 0.2 * r_max
    mid_mask = (radii > 0.2 * r_max) & (radii <= 0.6 * r_max)
    high_mask = radii > 0.6 * r_max

    total_energy = float(power.sum()) + 1e-12
    low_ratio = float(power[low_mask].sum() / total_energy)
    mid_ratio = float(power[mid_mask].sum() / total_energy)
    high_ratio = float(power[high_mask].sum() / total_energy)

    return low_ratio, mid_ratio, high_ratio


def _spectral_centroid(power: np.ndarray) -> float:
    h, w = power.shape
    cy, cx = h // 2, w // 2
    yy, xx = np.indices((h, w))
    radii = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)

    weighted_sum = float((radii * power).sum())
    total = float(power.sum()) + 1e-12
    return weighted_sum / total


def _anisotropy(power: np.ndarray) -> float:
    h, w = power.shape
    cy, cx = h // 2, w // 2
    yy, xx = np.indices((h, w))

    x = xx - cx
    y = yy - cy

    cov_xx = float((power * (x ** 2)).sum())
    cov_yy = float((power * (y ** 2)).sum())
    cov_xy = float((power * (x * y)).sum())
    mat = np.array([[cov_xx, cov_xy], [cov_xy, cov_yy]], dtype=np.float64)

    eigvals = np.linalg.eigvalsh(mat)
    eigvals = np.clip(eigvals, 1e-12, None)
    return float(eigvals[-1] / eigvals[0])


def extract_fft_features(image: np.ndarray, bins: int = 64) -> FourierFeatureSet:
    _, log_magnitude = compute_fft_spectrum(image)
    power = np.expm1(log_magnitude)
    power = power ** 2

    radial = _radial_profile(power, bins=bins)
    low_ratio, mid_ratio, high_ratio = _frequency_band_ratios(power)
    centroid = _spectral_centroid(power)
    anisotropy = _anisotropy(power)

    return FourierFeatureSet(
        radial_profile=radial,
        low_energy_ratio=low_ratio,
        mid_energy_ratio=mid_ratio,
        high_energy_ratio=high_ratio,
        spectral_centroid=centroid,
        anisotropy=anisotropy,
    )


def save_fft_only(log_magnitude: np.ndarray, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(log_magnitude, cmap="magma")
    ax.set_title("Log magnitude spectrum")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def save_side_by_side(image: np.ndarray, log_magnitude: np.ndarray, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].imshow(image, cmap="gray")
    axes[0].set_title("Before (input image)")
    axes[0].axis("off")

    axes[1].imshow(log_magnitude, cmap="magma")
    axes[1].set_title("After (Fourier magnitude)")
    axes[1].axis("off")

    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
