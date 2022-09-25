# %%
import whisper
import datetime
import torch
from time import gmtime, strftime


def transcribe_start(model_type, file_path, language_input, task="transcribe"):
    # print(model_type, file_path, language_input)
    language = None if language_input == "auto" else language_input

    model = whisper.load_model(model_type)

    print(model.device)

    result = model.transcribe(file_path, language=language, task=task, verbose=False)
    # print(result["text"])
    path = "{}.srt".format(strftime("%Y%m%d-%H%M%S", gmtime()))
    # print(__file__)
    with open(path, "w", encoding="UTF-8") as f:
        for seg in result["segments"]:
            id = seg["id"]
            start = (
                str(datetime.timedelta(seconds=round(seg["start"])))
                + ","
                + str(seg["start"] % 1)[2:5]
            )
            end = (
                str(datetime.timedelta(seconds=round(seg["end"])))
                + ","
                + str(seg["end"] % 1)[2:5]
            )
            text = seg["text"]
            f.write(f"{id}\n{start} --> {end}\n{text}\n\n")

    # del result
    # model.to("cpu")

    del model.encoder
    del model.decoder

    torch.cuda.empty_cache()

    return path


# "transcribe","translate"
transcribe_start("large", "mp4/jp2.mp4", "ja", "translate")
