# %%
import subprocess
from pathlib import Path

import torch
import whisper_timestamped

from src.utils.constants import DEVICE_TYPES, LANGUAGE_CODES, MODEL_TYPES, TASK_TYPES
from src.utils.helpers import write_srt, clean_filepath


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
        clean_subtitle = clean_filepath(subtitle)

        subtitle_path = Path(clean_subtitle).with_suffix(".srt")

        Path(subtitle_path).parent.mkdir(parents=True, exist_ok=True)

        if str(Path(subtitle_path).parent) == ".":
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
    if device == "cuda":
        if not torch.cuda.is_available():
            device = "cpu"
            print(f"Warning. GPU acceleration unavailable. Switch to CPU mode.")
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
    if vocal_extracter:
        demucs_directory = Path(subtitle_path).with_suffix("").name

        # "demucs --two-stems=vocals mp4/1min.mp4 -o tmp/ --filename {track}/{stem}.{ext}"" # FileName/VOCAL.wav
        cmd = rf'demucs --two-stems=vocals "{media}" -o "./tmp/{demucs_directory}/" --filename "{{stem}}.{{ext}}"'

        try:
            subprocess.run(cmd, check=True)
        except Exception as e:
            raise Exception(
                f"Error. Vocal extracter unavailable. Received: {cmd} \nError Code: {e}"
            )

        media = f"./tmp/{demucs_directory}/htdemucs/vocals.wav"

    # Whisper transcribe
    print("Debug: ", media, subtitle_path, model_type, language, task, device)

    whisper_model = whisper_timestamped.load_model(model_type, device=device)

    result = whisper_timestamped.transcribe(
        model=whisper_model,
        audio=media,
        language=language,
        task=task,
        vad=vad,
        verbose=False,
    )

    write_srt(result["segments"], subtitle_path)

    # Clear model memory
    del whisper_model.encoder
    del whisper_model.decoder
    torch.cuda.empty_cache()

    return subtitle_path
