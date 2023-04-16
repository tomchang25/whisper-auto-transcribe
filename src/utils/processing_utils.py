# From moviepy 2.0
import os
import shutil

from pydub import AudioSegment

OS_NAME = os.name


def ffmpeg_installed() -> bool:
    return shutil.which("ffmpeg") is not None


def audio_from_file(filename: str) -> AudioSegment:
    try:
        audio = AudioSegment.from_file(filename)
    except FileNotFoundError:
        raise ValueError(
            f"Cannot load audio from file: `{filename}` not found. Do you forgot to install `ffmpeg`."
        )

    return audio
