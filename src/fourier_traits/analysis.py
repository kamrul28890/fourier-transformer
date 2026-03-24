from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from .fourier import extract_fft_features, load_grayscale_image


@dataclass
class AnalysisResult:
    feature_table_path: Path
    cluster_table_path: Path
    summary_path: Path
    scatter_plot_path: Path


def _iter_images(folder: str | Path) -> list[Path]:
    folder = Path(folder)
    exts = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
    return sorted([p for p in folder.rglob("*") if p.suffix.lower() in exts])


def _trait_names(bins: int) -> list[str]:
    names = [f"radial_bin_{i:02d}" for i in range(bins)]
    names.extend(
        [
            "low_energy_ratio",
            "mid_energy_ratio",
            "high_energy_ratio",
            "spectral_centroid",
            "anisotropy",
        ]
    )
    return names


def analyze_image_folder(
    images_dir: str | Path,
    output_dir: str | Path,
    bins: int = 64,
    n_clusters: int = 5,
    random_state: int = 42,
) -> AnalysisResult:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    image_paths = _iter_images(images_dir)
    if not image_paths:
        raise ValueError(f"No images found under: {images_dir}")

    vectors: list[np.ndarray] = []
    rows: list[dict[str, float | str]] = []

    for path in image_paths:
        image = load_grayscale_image(path)
        features = extract_fft_features(image, bins=bins)
        vector = features.to_vector()

        vectors.append(vector)
        row = {"image_path": str(path)}
        for name, value in zip(_trait_names(bins), vector, strict=True):
            row[name] = float(value)
        rows.append(row)

    feature_matrix = np.vstack(vectors)
    feature_df = pd.DataFrame(rows)

    scaler = StandardScaler()
    scaled = scaler.fit_transform(feature_matrix)

    cluster_count = max(2, min(n_clusters, len(image_paths)))
    kmeans = KMeans(n_clusters=cluster_count, random_state=random_state, n_init="auto")
    labels = kmeans.fit_predict(scaled)

    pca = PCA(n_components=2, random_state=random_state)
    coords = pca.fit_transform(scaled)

    feature_df["cluster"] = labels
    feature_df["pca_x"] = coords[:, 0]
    feature_df["pca_y"] = coords[:, 1]

    silhouette = float(silhouette_score(scaled, labels)) if cluster_count > 1 and len(image_paths) > cluster_count else None

    cluster_table = (
        feature_df.groupby("cluster")
        .agg(
            image_count=("image_path", "count"),
            mean_low_energy=("low_energy_ratio", "mean"),
            mean_mid_energy=("mid_energy_ratio", "mean"),
            mean_high_energy=("high_energy_ratio", "mean"),
            mean_centroid=("spectral_centroid", "mean"),
            mean_anisotropy=("anisotropy", "mean"),
        )
        .reset_index()
    )

    feature_table_path = output_dir / "fft_features.csv"
    cluster_table_path = output_dir / "cluster_summary.csv"
    summary_path = output_dir / "analysis_summary.json"
    scatter_plot_path = output_dir / "cluster_scatter.png"

    feature_df.to_csv(feature_table_path, index=False)
    cluster_table.to_csv(cluster_table_path, index=False)

    summary = {
        "images_analyzed": len(image_paths),
        "feature_count": feature_matrix.shape[1],
        "cluster_count": int(cluster_count),
        "silhouette_score": silhouette,
        "pca_explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
        "cluster_traits": cluster_table.to_dict(orient="records"),
    }
    summary_path.write_text(json.dumps(summary, indent=2))

    fig, ax = plt.subplots(figsize=(8, 6))
    sc = ax.scatter(coords[:, 0], coords[:, 1], c=labels, cmap="tab10", alpha=0.8)
    ax.set_title("PCA projection of FFT features")
    ax.set_xlabel("PC 1")
    ax.set_ylabel("PC 2")
    fig.colorbar(sc, ax=ax, label="Cluster")
    fig.tight_layout()
    fig.savefig(scatter_plot_path, dpi=180)
    plt.close(fig)

    return AnalysisResult(
        feature_table_path=feature_table_path,
        cluster_table_path=cluster_table_path,
        summary_path=summary_path,
        scatter_plot_path=scatter_plot_path,
    )


def analysis_result_to_dict(result: AnalysisResult) -> dict[str, str]:
    return {k: str(v) for k, v in asdict(result).items()}
