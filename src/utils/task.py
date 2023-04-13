# %%
import subprocess
from pathlib import Path

import torch
import whisper_timestamped as whisper

from src.utils.constants import DEVICE_TYPES, LANGUAGE_CODES, MODEL_TYPES, TASK_TYPES
from src.utils.helpers import write_srt


def transcribe(
    media,
    *,
    subtitle=None,
    vocal_extracter=True,
    vad=True,
    language="auto",
    model_type="tiny",
    device="cpu",
    task="transcribe",
):
    # Input preprocess
    Path("tmp").mkdir(parents=True, exist_ok=True)

    if subtitle is None:
        subtitle_path = "tmp/{}".format(Path(media).with_suffix(".srt").name)
    else:
        subtitle_path = Path(subtitle).with_suffix(".srt")
        Path(subtitle_path).parent.mkdir(parents=True, exist_ok=True)

        if str(Path(subtitle).parent) == ".":
            subtitle_path = f"tmp/{subtitle_path}"

    if language == "auto":
        language = None
    elif language not in [x[0] for x in LANGUAGE_CODES]:
        raise ValueError(
            f"Invalid value for parameter `language`: {language}. Expected a supported language by openai-whisper"
        )

    valid_model_types = MODEL_TYPES
    if model_type not in valid_model_types:
        raise ValueError(
            f"Invalid value for parameter `device`: {device}. Please choose from one of: {valid_model_types}"
        )

    valid_devices = DEVICE_TYPES
    if device == "gpu":
        if not torch.cuda.is_available():
            raise Exception(f"Error. GPU acceleration unavailable")
    elif device not in valid_devices:
        raise ValueError(
            f"Invalid value for parameter `device`: {device}. Please choose from one of: {valid_devices}"
        )

    valid_tasks = TASK_TYPES
    if task not in valid_tasks:
        raise ValueError(
            f"Invalid value for parameter `task`: {task}. Please choose from one of: {valid_tasks}"
        )

    if language == "en" and model_type != "large":
        model_type += ".en"

    # Data preprocess
    vocal_extracter
    vad

    # Whisper transcribe
    print("Debug: ", media, subtitle_path, model_type, language, task, device)

    whisper_model = whisper.load_model(model_type, device=device)

    result = whisper_model.transcribe(
        media, language=language, task=task, verbose=False
    )

    write_srt(result["segments"], subtitle_path)

    # Clear model memory
    del whisper_model.encoder
    del whisper_model.decoder
    torch.cuda.empty_cache()

    return subtitle_path


# # %%
# from pathlib import Path
#
# Path("tmp\\A\\B\\C\\DDD.srt").parent.mkdir(parents=True, exist_ok=True)
