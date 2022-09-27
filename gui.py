# %%
from language import lang2index, lang2name
import gradio as gr
from trans import transcribe_start
import torch

precision2model = ["tiny", "base", "small", "medium", "large"]


def change_task_type(task_type):
    return gr.update(value=task_type)


def change_type(file_type):
    if file_type == "Video":
        return [gr.update(visible=True), gr.update(visible=False)]
    elif file_type == "Audio":
        return [gr.update(visible=False), gr.update(visible=True)]


def transcribe_submit(
    language_input,
    precision,
    file_type,
    video_input,
    audio_input,
    device,
    time_slice,
    task_type,
):
    output_type = [None, None]
    if file_type == "Video":
        input_file = video_input
    elif file_type == "Audio":
        input_file = audio_input

    model = precision2model[precision - 1]
    if lang2index[language_input] == "en":
        # print("EN")
        model += ".en"

    if device == "GPU":
        if torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"
    elif device == "CPU":
        device = "cpu"

    language = (
        None if lang2index[language_input] == "auto" else lang2index[language_input]
    )

    srt_path, result = transcribe_start(
        model_type=model,
        file_path=input_file,
        language=language,
        task=task_type.lower(),
        device=device,
    )

    return output_type + [
        gr.update(value="Done", visible=True),
        gr.update(value=srt_path, visible=True),
    ]

    # return output_type + [
    #     result,
    #     gr.update(value=srt_path, visible=True),
    # ]


device = "GPU" if torch.cuda.is_available() else "CPU"
# GUI Setup
with gr.Blocks() as demo:
    with gr.Row():
        language_input = gr.Dropdown(
            label="Language",
            value="Auto",
            choices=lang2name,
            type="index",
            interactive=True,
        )

        precision = gr.Slider(
            minimum=1,
            maximum=5,
            step=1,
            value=3,
            interactive=True,
            label="Precision",
        )

        file_type = gr.Radio(
            ["Video", "Audio"],
            value="Video",
            label="File Type",
            interactive=True,
        )
    with gr.Row():
        device = gr.Radio(
            label="Device",
            value=device,
            choices=["CPU", "GPU"],
            interactive=device == "GPU",
        )

        time_slice = gr.Slider(
            minimum=0,
            maximum=30,
            step=1,
            value=0,
            interactive=False,
            label="Time Slice",
        )

        task_type = gr.Radio(
            ["Transcribe", "Translate"],
            value="Transcribe",
            label="Task Type",
            interactive=True,
        )
    with gr.Row():
        with gr.Column():
            video_input = gr.Video(
                label="Video File", interactive=True, mirror_webcam=False
            )
            audio_input = gr.Audio(
                label="Audio File", interactive=True, type="filepath", visible=False
            )
            submit_btn = gr.Button("Transcribe")

    with gr.Row():
        with gr.Column():
            video_output = gr.Video(label="Demo", interactive=False, visible=False)
            audio_output = gr.Audio(label="Demo", interactive=False, visible=False)
            subtitle_output = gr.Text(
                label="Demo",
                value="Drag the file and click button!",
                interactive=False,
                visible=True,
            )
            srt_output = gr.File(interactive=False, visible=False)

    file_type.change(
        fn=change_type,
        inputs=[file_type],
        outputs=[video_input, audio_input],
    )

    task_type.change(
        fn=change_task_type,
        inputs=[task_type],
        outputs=[submit_btn],
    )

    submit_btn.click(
        fn=transcribe_submit,
        inputs=[
            language_input,
            precision,
            file_type,
            video_input,
            audio_input,
            device,
            time_slice,
            task_type,
        ],
        outputs=[video_output, audio_output, subtitle_output, srt_output],
    )

    # demo_play.play()

demo.launch()

# %%
