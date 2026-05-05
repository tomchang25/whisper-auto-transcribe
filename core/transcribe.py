from pathlib import Path
from typing import Callable, Optional, Union

from core.types import Segment


def run(
    audio_path: Union[str, Path],
    *,
    model_size: str = "medium",
    language: Optional[str] = None,
    task: str = "transcribe",
    device: str = "cpu",
    compute_type: str = "default",
    vad: bool = True,
    progress: Optional[Callable[[float], None]] = None,
) -> list[Segment]:
    from faster_whisper import WhisperModel

    model = WhisperModel(model_size, device=device, compute_type=compute_type)

    segments_iter, info = model.transcribe(
        str(audio_path),
        language=language,
        task=task,
        vad_filter=vad,
        beam_size=5,
    )

    duration = info.duration or 0.0
    results: list[Segment] = []
    for seg in segments_iter:
        results.append(Segment(start=seg.start, end=seg.end, text=seg.text))
        if progress is not None and duration > 0:
            progress(min(seg.end / duration, 1.0))

    if progress is not None:
        progress(1.0)

    return results
