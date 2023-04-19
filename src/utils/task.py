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
    MODEL_SIZES,
    TASK_TYPES,
    TRANSCRIBE_MODEL_TYPES,
    TEMPDIR,
)
from src.utils.helpers import clean_filepath, write_srt


def vocal_extracter(media, *, delete_tempfile=True):
    # Rename the original file to the new file name
    media_extension = Path(media).suffix
    media_new_filepath = TEMPDIR / Path("ve_temp").with_suffix(media_extension)
    shutil.copy(media, media_new_filepath)

    # TODO: Check hash before demucs to skip if hash is correct in project mode

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

    output_filename = f"{demucs_directory}/htdemucs/vocals.wav"

    return output_filename


def transcribe(
    media,
    *,
    subtitle_filename=None,
    vad=True,
    language="auto",
    model_size="tiny",
    device="cuda",
    task_type="transcribe",
    transcribe_model="whisper",
):
    # Whisper transcribe
    print(
        "Debug: ",
        media,
        subtitle_filename,
        transcribe_model,
        model_size,
        language,
        task_type,
        device,
    )

    if transcribe_model == "whisper":
        used_model = whisper.load_model(model_size, device=device)
        result = whisper.transcribe(
            model=used_model,
            audio=media,
            language=language,
            task=task_type,
            verbose=False,
        )

        write_srt(result["segments"], subtitle_filename)

    elif transcribe_model == "whisper_timestamps":
        used_model = whisper_timestamped.load_model(model_size, device=device)
        result = whisper_timestamped.transcribe(
            model=used_model,
            audio=media,
            language=language,
            task=task_type,
            vad=vad,
            verbose=False,
        )

        write_srt(result["segments"], subtitle_filename)

    elif transcribe_model == "stable_whisper":
        used_model = stable_whisper.load_model(model_size, device=device)

        result = used_model.transcribe(
            audio=media,
            language=language,
            task=task_type,
            vad=vad,
            verbose=False,
        )

        result.to_srt_vtt(subtitle_filename)

    # Clear model memory
    del used_model.encoder
    del used_model.decoder
    torch.cuda.empty_cache()


def start_task(
    media,
    *,
    subtitle=None,
    ve=True,
    vad=True,
    language="auto",
    model_size="tiny",
    device="cuda",
    task_type="transcribe",
    delete_tempfile=True,
    transcribe_model="whisper",
):
    if subtitle is None:
        subtitle_path = Path(media).with_suffix(".srt")
    else:
        clean_subtitle = clean_filepath(subtitle)
        subtitle_path = Path(clean_subtitle).with_suffix(".srt")

    if str(Path(subtitle_path).parent) == ".":
        subtitle_path = TEMPDIR / "subtitle_output" / subtitle_path.with_suffix(".srt")
        # subtitle_path = (
        #     TEMPDIR / subtitle_path.with_suffix("") / subtitle_path.with_suffix(".srt")
        # )

    subtitle_output = str(subtitle_path)

    if language == "auto":
        language = None
    elif language not in [x[0] for x in LANGUAGE_CODES]:
        raise ValueError(
            f"Invalid value for parameter `language`: {language}. Expected a supported language by openai-whisper"
        )

    valid_model_sizes = MODEL_SIZES
    if model_size not in valid_model_sizes:
        raise ValueError(
            f"Invalid value for parameter `model_size`: {model_size}. Please choose from one of: {valid_model_sizes}"
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

    valid_task_types = TASK_TYPES
    if task_type not in valid_task_types:
        raise ValueError(
            f"Invalid value for parameter `task`: {task_type}. Please choose from one of: {valid_task_types}"
        )

    valid_transcribe_model = TRANSCRIBE_MODEL_TYPES
    if transcribe_model not in valid_transcribe_model:
        raise ValueError(
            f"Invalid value for parameter `transcribe_model`: {transcribe_model}. Please choose from one of: {valid_transcribe_model}"
        )

    if language == "en" and model_size != "large":
        model_size += ".en"

    # Data preprocess
    if ve:
        media = vocal_extracter(media)

    # Whisper transcribe
    transcribe(
        media,
        subtitle_filename=subtitle_output,
        language=language,
        model_size=model_size,
        device=device,
        task_type=task_type,
        transcribe_model=transcribe_model,
        vad=vad,
    )

    return subtitle_output
