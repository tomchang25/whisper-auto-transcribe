import argparse
from trans import easy_task


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
        help="Task mode [translate, transcribe] Default [translate].",
        required=False,
        default="translate",
    )

    parser.add_argument(
        "--device",
        metavar="device",
        type=str,
        help="Use device. [auto, cpu, cuda] Default [auto].",
        required=False,
        default="auto",
    )

    parser.add_argument(
        "--model",
        metavar="model",
        type=str,
        help="Use model. [tiny, base, small, medium, large] Default [base].",
        required=False,
        default="base",
    )

    args = parser.parse_args()
    res, used_time = easy_task(
        model_type=args.model,
        file_path=args.input,
        language=args.language,
        task=args.task,
        output_path=args.output,
        device=args.device,
    )

    print(
        ("[{used_time:.3f}] take, {task} file is found at [{file_path}].\n").format(
            used_time=used_time, file_path=res, task=args.task
        )
    )


if __name__ == "__main__":
    cli()
