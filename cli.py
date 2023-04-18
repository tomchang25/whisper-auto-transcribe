import argparse
from src.utils.task import transcribe
from pathlib import Path
import mimetypes


def cli():
    parser = argparse.ArgumentParser(description="Whisper Auto Transcribe")

    parser.add_argument(
        "input",
        metavar="input",
        type=str,
        help="Input video file(s) or directory containing video files. If a directory is specified, batch work will be performed on all files in the directory.",
    )

    parser.add_argument(
        "--output",
        metavar="output",
        type=str,
        help="Output file name or directory. ",
        required=True,
    )

    parser.add_argument(
        "-lang",
        "--language",
        metavar="language",
        type=str,
        help="Input lanuage code [ISO 639-1]. Default [auto].",
        required=False,
        default="auto",
    )

    parser.add_argument(
        "--task",
        metavar="task",
        type=str,
        help="Task mode [translate, transcribe] Default [transcribe].",
        required=False,
        default="transcribe",
    )

    parser.add_argument(
        "--device",
        metavar="device",
        type=str,
        help="Use device. [cpu, cuda] Default [cuda].",
        required=False,
        default="cuda",
    )

    parser.add_argument(
        "--transcribe-model",
        metavar="transcribe_model",
        type=str,
        help="Use model. [whisper, whisper_timestamps, stable_whisper] Default [stable_whisper].",
        required=False,
        default="stable_whisper",
    )

    parser.add_argument(
        "--remain-tempfile",
        action="store_true",
        help="Keep temporary file after processing. Default is False.",
        required=False,
        default=False,
    )

    parser.add_argument(
        "--no-vad",
        action="no_vad",
        help="Not use VAD. Default is False.",
        required=False,
        default=False,
    )

    parser.add_argument(
        "--no-ve",
        action="no_ve",
        help="Not use vocal extracter. Default is False.",
        required=False,
        default=False,
    )

    model_size_group = parser.add_mutually_exclusive_group()

    model_size_group.add_argument(
        "--model-size",
        metavar="model_size",
        type=str,
        help="Use model size. [tiny, base, small, medium, large] Default [medium].",
        required=False,
        default="medium",
    )

    model_size_group.add_argument(
        "--model",
        metavar="model",
        type=str,
        help="Use model size. [tiny, base, small, medium, large] Default [medium].",
        required=False,
        default="medium",
    )

    args = parser.parse_args()
    input_path = Path(args.input)
    delete_tempfile = not args.remain_tempfile

    if input_path.is_dir():
        # Batch mode - process all videos in the input directory
        output_dir = Path(args.output)
        for media_file in input_path.glob("*"):
            media_file_type = mimetypes.guess_type(media_file)[0]
            if (
                media_file_type
                and "audio" in media_file_type
                or "video" in media_file_type
            ):
                subtitle_path = output_dir / (media_file.stem + ".srt")
                transcribe(
                    str(media_file),
                    subtitle=str(subtitle_path),
                    language=args.language,
                    model_type=args.model_size,
                    transcribe_model=args.transcribe_model,
                    device=args.device,
                    task=args.task,
                    delete_tempfile=delete_tempfile,
                    vad=not args.no_vad,
                    vocal_extracter=not args.no_ve,
                )
            else:
                print(f"Skip. Can't transcribe file: {media_file}")
    else:
        media_file = args.input
        media_file_type = mimetypes.guess_type(media_file)[0]
        if media_file_type and "audio" in media_file_type or "video" in media_file_type:
            subtitle_path = transcribe(
                args.input,
                subtitle=args.output,
                language=args.language,
                model_type=args.model_size,
                transcribe_model=args.transcribe_model,
                device=args.device,
                task=args.task,
                delete_tempfile=delete_tempfile,
                vad=not args.no_vad,
                vocal_extracter=not args.no_ve,
            )
        else:
            print(f"Skip. Can't transcribe file: {media_file}")


# python cli.py mp4/1min.mp4 --output out/final.srt --model-size large --remain-tempfile
# python cli.py test_mp4 --output out/batch --model-size large

if __name__ == "__main__":
    cli()
