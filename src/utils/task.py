# %%
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

import stable_whisper
import torch
import whisper
import whisper_timestamped

from src.utils.constants import (
    DEVICE_TYPES,
    LANGUAGE_CODES,
    MODEL_TYPES,
    TASK_TYPES,
    TRANSCRIBE_MODEL_TYPES,
)
from src.utils.helpers import clean_filepath, write_srt


def transcribe(
    media,
    *,
    subtitle=None,
    vocal_extracter=True,
    vad=True,
    language="auto",
    model_type="tiny",
    device="cuda",
    task="transcribe",
    delete_tempfile=True,
    transcribe_model="whisper",
):
    if subtitle is None:
        subtitle_path = Path(media).with_suffix(".srt")
    else:
        clean_subtitle = clean_filepath(subtitle)
        subtitle_path = Path(clean_subtitle).with_suffix(".srt")

    if str(Path(subtitle_path).parent) == ".":
        subtitle_path = (
            "tmp" / subtitle_path.with_suffix("") / subtitle_path.with_suffix(".srt")
        )

    Path(subtitle_path).parent.mkdir(parents=True, exist_ok=True)
    subtitle_path = str(subtitle_path)

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

    valid_transcribe_model = TRANSCRIBE_MODEL_TYPES
    if transcribe_model not in valid_transcribe_model:
        raise ValueError(
            f"Invalid value for parameter `transcribe_model`: {transcribe_model}. Please choose from one of: {valid_transcribe_model}"
        )

    if language == "en" and model_type != "large":
        model_type += ".en"

    # Data preprocess
    if vocal_extracter:
        # Rename the original file to the new file name
        media_extension = Path(media).suffix
        media_new_filepath = tempfile.gettempdir() / Path(
            "tempfreesubtitle/main"
        ).with_suffix(media_extension)

        Path(media_new_filepath).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(media, media_new_filepath)

        if delete_tempfile:
            demucs_directory = tempfile.gettempdir() / Path("tempfreesubtitle")
        else:
            demucs_directory = "tmp/" + datetime.now().strftime(r"%Y-%m-%d %H-%M-%S")

        # "demucs --two-stems=vocals mp4/1min.mp4 -o tmp/ --filename {track}/{stem}.{ext}"" # FileName/VOCAL.wav
        cmd = rf'demucs --two-stems=vocals "{media_new_filepath}" -o "{demucs_directory}" --filename "{{stem}}.{{ext}}"'

        try:
            subprocess.run(cmd, check=True)
        except Exception as e:
            raise Exception(
                f"Error. Vocal extracter unavailable. Received: \n{media}, {media_new_filepath}, {demucs_directory}\n{cmd}"
            )

        media = f"{demucs_directory}/htdemucs/vocals.wav"

    # Whisper transcribe
    print(
        "Debug: ",
        media,
        subtitle_path,
        transcribe_model,
        model_type,
        language,
        task,
        device,
    )

    if transcribe_model == "whisper":
        used_model = whisper.load_model(model_type, device=device)
        result = whisper.transcribe(
            model=used_model,
            audio=media,
            language=language,
            task=task,
            verbose=False,
        )

        write_srt(result["segments"], subtitle_path)

    elif transcribe_model == "whisper_timestamps":
        used_model = whisper_timestamped.load_model(model_type, device=device)
        result = whisper_timestamped.transcribe(
            model=used_model,
            audio=media,
            language=language,
            task=task,
            vad=vad,
            verbose=False,
        )

        write_srt(result["segments"], subtitle_path)

    elif transcribe_model == "stable_whisper":
        used_model = stable_whisper.load_model(model_type, device=device)

        result = used_model.transcribe(
            audio=media,
            language=language,
            task=task,
            vad=vad,
            verbose=False,
        )

        result.to_srt_vtt(subtitle_path)

    # Clear model memory
    del used_model.encoder
    del used_model.decoder
    torch.cuda.empty_cache()

    return subtitle_path
