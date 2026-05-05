from pathlib import Path
from typing import Union


def download(url: str, dest_dir: Union[str, Path]) -> Path:
    if not url or not url.strip():
        raise ValueError("URL is empty")

    from yt_dlp import YoutubeDL

    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "format": "mp4",
        "outtmpl": str(dest_dir / "%(title)s.%(ext)s"),
        "quiet": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return Path(ydl.prepare_filename(info))
