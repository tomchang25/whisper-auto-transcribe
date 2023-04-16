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
            if (
                mimetypes.guess_type(media_file)[0]
                and "audio" in mimetypes.guess_type(media_file)[0]
                or "video" in mimetypes.guess_type(media_file)[0]
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
        # Single file mode - process the input video file
        subtitle_path = transcribe(
            args.input,
            subtitle=args.output,
            language=args.language,
            model_type=args.model,
            device=args.device,
            task=args.task,
        )

    print(
        ("[{task} file is found at [{subtitle_path}].\n").format(
            task=args.task, subtitle_path=subtitle_path
        )
    )


# python cli.py mp4/1min.mp4 --output out/final.srt --model large
# python cli.py mp4 --output tmp/mp4 --model large

if __name__ == "__main__":
    cli()
