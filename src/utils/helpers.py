from typing import Iterator, TextIO


def convert_to_seconds(time):
    """Will convert any time into seconds.
    If the type of `time` is not valid,
    it's returned as is.
    Here are the accepted formats:
    >>> convert_to_seconds(15.4)   # seconds
    15.4
    >>> convert_to_seconds((1, 21.5))   # (min,sec)
    81.5
    >>> convert_to_seconds((1, 1, 2))   # (hr, min, sec)
    3662
    >>> convert_to_seconds('01:01:33.045')
    3693.045
    >>> convert_to_seconds('01:01:33,5')    # coma works too
    3693.5
    >>> convert_to_seconds('1:33,5')    # only minutes and secs
    99.5
    >>> convert_to_seconds('33.5')      # only secs
    33.5
    """
    factors = (1, 60, 3600)

    if isinstance(time, str):
        time = [float(part.replace(",", ".")) for part in time.split(":")]

    if not isinstance(time, (tuple, list)):
        return time

    return sum(mult * part for mult, part in zip(factors, reversed(time)))


def clean_filepath(filepath):
    # Use str.maketrans() and str.translate() to remove disallowed characters
    disallowed = "*?<>|"
    translation_table = str.maketrans("", "", disallowed)
    clean_filepath = filepath.translate(translation_table)

    return clean_filepath


def format_timestamp(seconds: float, always_include_hours: bool = False):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def write_srt(transcript: Iterator[dict], file: TextIO):
    """
    Write a transcript to a file in SRT format.
    Example usage:
        from pathlib import Path
        from whisper.utils import write_srt
        result = transcribe(model, audio_path, temperature=temperature, **args)
        # save SRT
        audio_basename = Path(audio_path).stem
        with open(Path(output_dir) / (audio_basename + ".srt"), "w", encoding="utf-8") as srt:
            write_srt(result["segments"], file=srt)
    """
    # TODO: Allow file as Path
    with open(file, "w", encoding="UTF-8") as f:
        for segment in transcript:
            # write srt lines
            id = segment["id"]
            start = format_timestamp(segment["start"], always_include_hours=True)
            end = format_timestamp(segment["end"], always_include_hours=True)
            text = segment["text"].strip().replace("-->", "->")

            f.write(f"{id}\n{start} --> {end}\n{text}\n\n")
