# %%
from pathlib import Path

import gradio as gr
import pysubs2
import torch
from yt_dlp import YoutubeDL

from language import lang2index, lang2name
from task import easy_task

precision2model = ["tiny", "base", "small", "medium", "large"]


def download_video(video_url):
    ydl_opts = {
        # "paths": {"home": "mp4/"},
        "format": "mp4",
        "outtmpl": "/mp4/%(title)s.%(ext)s",
        "quiet": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        filename = ydl.prepare_filename(info)

    return [gr.update(value=filename), filename]


def change_task_type(task_type):
    return gr.update(value=task_type)


def change_type(file_type):
    if file_type == "Video":
        return [
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=True),
        ]
    elif file_type == "Audio":
        return [
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=False),
        ]


def transcribe_submit(
    language_input,
    precision,
    file_type,
    video_input,
    audio_input,
    device,
    time_slice,
    task_type,
    video_name,
    # progress=gr.Progress(),
):
    # progress(0, desc="Starting")
    if file_type == "Video":
        input_file = video_input
    elif file_type == "Audio":
        input_file = audio_input

    if video_name is None:
        video_name = input_file

    srt_file_name = "tmp/" + Path(video_name).stem + ".srt"
    vtt_file_name = "tmp/" + Path(video_name).stem + ".vtt"
    ass_file_name = "tmp/" + Path(video_name).stem + ".ass"

    model = precision2model[precision - 1]

    easy_task(
        model_type=model,
        file_path=input_file,
        output_path=srt_file_name,
        language=lang2index[language_input],
        task=task_type.lower(),
        device=device.lower(),
    )

    print(srt_file_name, vtt_file_name, ass_file_name)

    subs = pysubs2.load(srt_file_name, encoding="utf-8")
    subs.save(vtt_file_name)
    subs.save(ass_file_name)

    subtitle_txt = "```" + subs.to_string("srt") + "```"

    # progress_txt, srt_output, result_tab
    return [
        "Finish",
        gr.update(selected="result_tab"),
        gr.update(value=srt_file_name),
        gr.update(value=vtt_file_name),
        gr.update(value=ass_file_name),
        gr.update(value=input_file, caption=srt_file_name),
        gr.update(value=subtitle_txt),
    ]


def gui():

    device = "GPU" if torch.cuda.is_available() else "CPU"
    with gr.Blocks() as demo:
        with gr.Tabs() as demo_tabs:
            with gr.Tab("Source", id="source_tab") as source_tab:
                with gr.Blocks():
                    with gr.Row():
                        file_type = gr.Radio(
                            ["Video", "Audio"],
                            value="Video",
                            label="File Type",
                            interactive=True,
                        )

                    with gr.Row() as url_row:
                        with gr.Box():
                            with gr.Column():
                                url_input = gr.Textbox(
                                    label="Youtbue URL", interactive=True
                                )
                            with gr.Column():
                                download_btn = gr.Button(value="Import video")
                                video_name = gr.State()
                    with gr.Row():
                        with gr.Column():
                            video_input = gr.Video(
                                label="Video File",
                                interactive=True,
                                mirror_webcam=False,
                            )

                            audio_input = gr.Audio(
                                label="Audio File",
                                interactive=True,
                                type="filepath",
                                visible=False,
                            )

            with gr.Tab("Setting", id="setting_tab") as setting_tab:
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
                    submit_btn = gr.Button("Transcribe")
                with gr.Row():
                    progress_txt = gr.Text(
                        label="Demo",
                        value="",
                        interactive=False,
                        visible=True,
                    )
            with gr.Tab("Result", id="result_tab") as result_tab:
                with gr.Row():
                    srt_download = gr.File(label="srt download", interactive=False)
                    vtt_download = gr.File(label="vtt download", interactive=False)
                    ass_download = gr.File(label="ass download", interactive=False)
                with gr.Row():
                    demo_video = gr.Video(
                        label="Demo",
                        interactive=False,
                    )
                with gr.Row():
                    with gr.Accordion("Subtitles", open=False):
                        demo_subtitle = gr.Markdown()

        file_type.change(
            fn=change_type,
            inputs=[file_type],
            outputs=[video_input, audio_input, url_row],
        )

        task_type.change(
            fn=change_task_type,
            inputs=[task_type],
            outputs=[submit_btn],
        )

        download_btn.click(
            fn=download_video, inputs=url_input, outputs=[video_input, video_name]
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
                video_name,
            ],
            outputs=[
                progress_txt,
                demo_tabs,
                srt_download,
                vtt_download,
                ass_download,
                demo_video,
                demo_subtitle,
            ],
        )

    return demo


def launch():
    gui().launch()


if __name__ == "__main__":
    launch()
# %%
