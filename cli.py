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
        "--model",
        metavar="model",
        type=str,
        help="Use model. [tiny, base, small, medium, large] Default [medium].",
        required=False,
        default="medium",
    )

    args = parser.parse_args()
    input_path = Path(args.input)

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
                    model_type=args.model,
                    device=args.device,
                    task=args.task,
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
                model_type=args.model,
                device=args.device,
                task=args.task,
            )
        else:
            print(f"Skip. Can't transcribe file: {media_file}")


# python cli.py mp4/1min.mp4 --output out/final.srt --model large
# python cli.py test_mp4 --output batch --model large

if __name__ == "__main__":
    cli()
