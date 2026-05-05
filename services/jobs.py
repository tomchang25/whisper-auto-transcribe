import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

from core import subtitles, transcribe, vocal_extract
from core.types import Segment


@dataclass
class TranscribeJob:
    input_path: Path
    output_path: Path
    language: Optional[str] = None
    model_size: str = "medium"
    device: str = "cpu"
    task: str = "transcribe"
    vocal_extraction: bool = True
    vad: bool = True
    formats: tuple[str, ...] = ("srt",)
    keep_temp: bool = False


@dataclass
class JobResult:
    segments: list[Segment]
    output_files: dict[str, Path] = field(default_factory=dict)


ProgressCb = Callable[[str, float], None]


def _resolve_work_dir(keep_temp: bool) -> Path:
    if keep_temp:
        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return Path("tmp") / stamp
    return Path(tempfile.gettempdir()) / "whisper-auto-transcribe"


def _emit(progress: Optional[ProgressCb], stage: str, fraction: float) -> None:
    if progress is not None:
        progress(stage, fraction)


def run_job(job: TranscribeJob, progress: Optional[ProgressCb] = None) -> JobResult:
    input_path = Path(job.input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    work_dir = _resolve_work_dir(job.keep_temp)
    audio_path: Path = input_path

    if job.vocal_extraction:
        _emit(progress, "vocal", 0.0)
        audio_path = vocal_extract.extract_vocals(input_path, work_dir)
        _emit(progress, "vocal", 1.0)

    _emit(progress, "transcribe", 0.0)
    segments = transcribe.run(
        audio_path,
        model_size=job.model_size,
        language=job.language,
        task=job.task,
        device=job.device,
        vad=job.vad,
        progress=lambda f: _emit(progress, "transcribe", f),
    )

    _emit(progress, "write", 0.0)
    output_path = Path(job.output_path)
    output_files: dict[str, Path] = {}
    n = max(len(job.formats), 1)
    for i, fmt in enumerate(job.formats, start=1):
        target = output_path.with_suffix(f".{fmt}")
        subtitles.write(segments, target, fmt)
        output_files[fmt] = target
        _emit(progress, "write", i / n)

    return JobResult(segments=segments, output_files=output_files)
