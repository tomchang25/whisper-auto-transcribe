import argparse
import mimetypes
import sys
from pathlib import Path

from services import TranscribeJob, run_job


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Whisper Auto Transcribe")
    parser.add_argument(
        "input",
        type=str,
        help="Input video/audio file or directory of media files for batch mode.",
    )
    parser.add_argument("--output", type=str, required=True, help="Output file path or directory.")
    parser.add_argument(
        "-lang", "--language", type=str, default="auto",
        help="ISO 639-1 language code, or 'auto' to detect.",
    )
    parser.add_argument(
        "--task", type=str, default="transcribe", choices=["transcribe", "translate"],
    )
    parser.add_argument(
        "--device", type=str, default="cpu", choices=["cpu", "cuda"],
    )
    parser.add_argument(
        "--model-size", type=str, default="medium",
        help="faster-whisper model size: tiny, base, small, medium, large-v1/v2/v3, distil-large-v3.",
    )
    parser.add_argument(
        "--no-vocal-extraction", action="store_true",
        help="Skip demucs vocal extraction; feed raw audio to the transcriber.",
    )
    parser.add_argument(
        "--remain-tempfile", action="store_true",
        help="Keep intermediate files after processing.",
    )
    return parser


def _is_media(path: Path) -> bool:
    mime = mimetypes.guess_type(str(path))[0]
    return bool(mime and ("audio" in mime or "video" in mime))


def _print_progress(stage: str, fraction: float) -> None:
    print(f"[{stage}] {fraction:.0%}", file=sys.stderr)


def _make_job(args, input_path: Path, output_path: Path) -> TranscribeJob:
    return TranscribeJob(
        input_path=input_path,
        output_path=output_path,
        language=None if args.language == "auto" else args.language,
        model_size=args.model_size,
        device=args.device,
        task=args.task,
        vocal_extraction=not args.no_vocal_extraction,
        keep_temp=args.remain_tempfile,
        formats=("srt",),
    )


def cli() -> None:
    args = _build_parser().parse_args()
    input_path = Path(args.input)

    if input_path.is_dir():
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for media_file in sorted(input_path.glob("*")):
            if not _is_media(media_file):
                print(f"Skip. Not a media file: {media_file}")
                continue
            job = _make_job(args, media_file, output_dir / media_file.stem)
            run_job(job, progress=_print_progress)
    else:
        if not _is_media(input_path):
            print(f"Skip. Not a media file: {input_path}")
            return
        output_path = Path(args.output)
        if output_path.suffix:
            output_path = output_path.with_suffix("")
        job = _make_job(args, input_path, output_path)
        run_job(job, progress=_print_progress)


if __name__ == "__main__":
    cli()
