import argparse
from src.utils.task import transcribe


def cli():
    parser = argparse.ArgumentParser(description="Whisper Auto Transcribe")

    parser.add_argument("input", metavar="input", type=str, help="Input video file")

    parser.add_argument(
        "--output", metavar="output", type=str, help="Output file name.", required=True
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

if __name__ == "__main__":
    cli()
