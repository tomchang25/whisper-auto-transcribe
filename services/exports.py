from pathlib import Path
from typing import Iterable, Union

from core import subtitles
from core.subtitles import SUPPORTED_FORMATS
from core.types import Segment


def save_subtitles(
    segments: Iterable[Segment],
    path: Union[str, Path],
    fmt: str,
) -> Path:
    return subtitles.write(segments, path, fmt)


__all__ = ["SUPPORTED_FORMATS", "save_subtitles"]
