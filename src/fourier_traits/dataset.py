from __future__ import annotations

import mimetypes
from pathlib import Path

import requests

WIKIMEDIA_API = "https://commons.wikimedia.org/w/api.php"


def search_wikimedia_image_urls(query: str, limit: int = 100) -> list[str]:
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": 6,
        "gsrlimit": min(limit, 500),
        "prop": "imageinfo",
        "iiprop": "url|mime",
    }

    response = requests.get(WIKIMEDIA_API, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    pages = data.get("query", {}).get("pages", {})
    urls: list[str] = []

    for page in pages.values():
        imageinfo = page.get("imageinfo", [])
        if not imageinfo:
            continue
        info = imageinfo[0]
        mime = info.get("mime", "")
        if not mime.startswith("image/"):
            continue
        url = info.get("url")
        if url:
            urls.append(url)

    return urls


def _safe_extension(content_type: str, fallback: str = ".jpg") -> str:
    ext = mimetypes.guess_extension(content_type.split(";")[0].strip())
    if ext in {".jpe", ".jpeg"}:
        return ".jpg"
    if ext is None:
        return fallback
    return ext


def download_images(urls: list[str], output_dir: str | Path, max_images: int) -> list[Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    saved: list[Path] = []
    for idx, url in enumerate(urls, start=1):
        if len(saved) >= max_images:
            break

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "image/jpeg")
            ext = _safe_extension(content_type)
            file_path = output_dir / f"image_{idx:04d}{ext}"
            file_path.write_bytes(response.content)
            saved.append(file_path)
        except requests.RequestException:
            continue

    return saved


def fetch_dataset_from_wikimedia(query: str, output_dir: str | Path, limit: int = 100) -> list[Path]:
    urls = search_wikimedia_image_urls(query=query, limit=max(limit * 2, 50))
    return download_images(urls=urls, output_dir=output_dir, max_images=limit)
