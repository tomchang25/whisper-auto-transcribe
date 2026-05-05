import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Union


def extract_vocals(media_path: Union[str, Path], work_dir: Union[str, Path]) -> Path:
    media_path = Path(media_path)
    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)

    staged = Path(tempfile.gettempdir()) / "whisper-auto-transcribe" / f"main{media_path.suffix}"
    staged.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(media_path, staged)

    cmd = [
        "demucs",
        "--two-stems=vocals",
        str(staged),
        "-o",
        str(work_dir),
        "--filename",
        "{stem}.{ext}",
    ]

    try:
        subprocess.run(cmd, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise RuntimeError(
            f"Vocal extraction failed for {media_path}. demucs command: {' '.join(cmd)}"
        ) from e

    vocals = work_dir / "htdemucs" / "vocals.wav"
    if not vocals.exists():
        raise RuntimeError(f"Expected vocals output not found at {vocals}")
    return vocals
