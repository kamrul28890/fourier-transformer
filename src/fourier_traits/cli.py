from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analysis import analysis_result_to_dict, analyze_image_folder
from .dataset import fetch_dataset_from_wikimedia
from .fourier import compute_fft_spectrum, load_grayscale_image, save_fft_visualization


def cmd_single(args: argparse.Namespace) -> None:
    image = load_grayscale_image(args.image)
    _, log_magnitude = compute_fft_spectrum(image)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / "single_fft_visualization.png"

    save_fft_visualization(image=image, log_magnitude=log_magnitude, output_path=output_path)
    print(json.dumps({"saved_visualization": str(output_path)}, indent=2))


def cmd_fetch(args: argparse.Namespace) -> None:
    saved_paths = fetch_dataset_from_wikimedia(
        query=args.query,
        output_dir=args.out_dir,
        limit=args.limit,
    )
    payload = {
        "query": args.query,
        "requested": args.limit,
        "downloaded": len(saved_paths),
        "output_dir": str(Path(args.out_dir).resolve()),
    }
    print(json.dumps(payload, indent=2))


def cmd_analyze(args: argparse.Namespace) -> None:
    result = analyze_image_folder(
        images_dir=args.images_dir,
        output_dir=args.out_dir,
        bins=args.bins,
        n_clusters=args.clusters,
    )
    print(json.dumps(analysis_result_to_dict(result), indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fourier-traits",
        description="Fourier-transform based image pattern analysis toolkit",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    single = sub.add_parser("single", help="Compute Fourier transform for one image")
    single.add_argument("--image", required=True, help="Path to an image file")
    single.add_argument("--out-dir", default="outputs/single", help="Directory for output images")
    single.set_defaults(func=cmd_single)

    fetch = sub.add_parser("fetch", help="Download an online image dataset from Wikimedia")
    fetch.add_argument("--query", required=True, help="Search query, e.g. 'cats' or 'city skyline'")
    fetch.add_argument("--limit", type=int, default=100, help="Number of images to download")
    fetch.add_argument("--out-dir", default="data/images", help="Where to save downloaded images")
    fetch.set_defaults(func=cmd_fetch)

    analyze = sub.add_parser("analyze", help="Run FFT pattern analysis across an image folder")
    analyze.add_argument("--images-dir", required=True, help="Folder containing images")
    analyze.add_argument("--out-dir", default="outputs/analysis", help="Directory for analysis artifacts")
    analyze.add_argument("--bins", type=int, default=64, help="Number of radial frequency bins")
    analyze.add_argument("--clusters", type=int, default=5, help="Number of clusters for trait grouping")
    analyze.set_defaults(func=cmd_analyze)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
