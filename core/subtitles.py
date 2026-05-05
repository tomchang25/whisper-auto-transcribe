import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, Union

from core.types import Segment

SUPPORTED_FORMATS = ("srt", "vtt", "ass", "json")


def write(
    segments: Iterable[Segment],
    path: Union[str, Path],
    fmt: str,
) -> Path:
    fmt = fmt.lower()
    if fmt not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported subtitle format {fmt!r}. Choose from {SUPPORTED_FORMATS}.")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    seg_list = list(segments)

    if fmt == "json":
        path.write_text(
            json.dumps([asdict(s) for s in seg_list], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path

    import pysubs2

    subs = pysubs2.SSAFile()
    for s in seg_list:
        subs.append(
            pysubs2.SSAEvent(
                start=int(s.start * 1000),
                end=int(s.end * 1000),
                text=s.text.strip(),
            )
        )
    subs.save(str(path), format_=fmt)
    return path
