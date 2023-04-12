# %%
import os
from pathlib import Path
from time import localtime, strftime, time

import torch
import whisper
from utils.helpers import write_srt
from language import lang2index


def easy_task(
    file_path,
    output_path=None,
    # output_format="srt",
    device="auto",
    language="auto",
    model_type="base",
    task="transcribe",
    slice_interval=0,
):
    # parameter
    try:
        if output_path is None:
            Path("./tmp").mkdir(parents=True, exist_ok=True)
            output_path = "./tmp/{}.srt".format(strftime("%Y%m%d-%H%M%S", localtime()))
        else:
            output_dir = os.path.dirname(output_path)
            Path(output_dir).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print("Unknown error: \n", e)
        return

    device = device.lower()
    if device == "auto" or device == "gpu":
        device = "cuda" if torch.cuda.is_available() else "cpu"
        if device == "gpu":
            print("Warning: GPU acceleration unavailable")

    if language == "auto":
        language = None
    elif language not in lang2index:
        print("Unknown language: \n", language)
        return

    if language == "en" and "en" not in model_type and model_type != "large":
        model_type += ".en"

    start_time = time()

    output_path, _ = task_start(
        file_path=file_path,
        output_path=output_path,
        # output_format=output_format,
        device=device,
        language=language,
        model_type=model_type,
        task=task,
    )

    return output_path, time() - start_time


def task_start(
    file_path,
    output_path,
    # output_format,
    device,
    language,
    model_type,
    task,
):
    # process
    model = whisper.load_model(model_type, device=device)

    print(model_type, file_path, language, task, device)
    print(model.device)

    result = model.transcribe(file_path, language=language, task=task, verbose=False)

    # print(__file__)
    with open(output_path, "w", encoding="UTF-8") as f:
        write_srt(result["segments"], output_path)

    # clear memory
    del model.encoder
    del model.decoder

    torch.cuda.empty_cache()

    return output_path, result


if __name__ == "__main__":
    res, used_time = easy_task(
        "mp4/en.mp4", "out/test/en.srt", model_type="small", task="transcribe"
    )
    print(used_time)
