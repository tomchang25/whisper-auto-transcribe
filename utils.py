from typing import Iterator, TextIO

# copy from whisper
# -----------------
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


# def write_txt(transcript: Iterator[dict], file: TextIO):
#     for segment in transcript:
#         print(segment["text"].strip(), file=file, flush=True)


# def write_vtt(transcript: Iterator[dict], file: TextIO):
#     print("WEBVTT\n", file=file)
#     for segment in transcript:
#         print(
#             f"{format_timestamp(segment['start'])} --> {format_timestamp(segment['end'])}\n"
#             f"{segment['text'].replace('-->', '->')}\n",
#             file=file,
#             flush=True,
#         )


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
    with open(file, "w", encoding="UTF-8") as f:
        for segment in transcript:
            # write srt lines
            id = segment["id"]
            start = format_timestamp(segment["start"], always_include_hours=True)
            end = format_timestamp(segment["end"], always_include_hours=True)
            text = segment["text"].strip().replace("-->", "->")

            f.write(f"{id}\n{start} --> {end}\n{text}\n\n")


# -----------------
