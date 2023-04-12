# %%
from pathlib import Path

import gradio as gr
import pysubs2
import torch
from yt_dlp import YoutubeDL
import os

from language import lang2index, lang2name
from task import easy_task


precision2model = ["tiny", "base", "small", "medium", "large"]


def change_task_type(task_type):
    return gr.update(value=task_type)


# def change_type(file_type):
#     if file_type == "Video":
#         return [
#             gr.update(visible=True),
#             gr.update(visible=False),
#             gr.update(visible=True),
#         ]
#     elif file_type == "Audio":
#         return [
#             gr.update(visible=False),
#             gr.update(visible=True),
#             gr.update(visible=False),
#         ]


def transcribe_submit(
    *,
    language_input,
    precision,
    file_type,
    video_input,
    audio_input,
    device,
    todo_function,
    task_type,
    video_name,
):
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
        gr.update(value=[input_file, srt_file_name]),
        gr.update(value=subtitle_txt),
    ]


def gui():
    device = "GPU" if torch.cuda.is_available() else "CPU"
    with gr.Blocks() as demo:
        with gr.Tabs() as demo_tabs:
            with gr.Tab("Source", id="source_tab") as source_tab:
                file_name = gr.Textbox()
                file_ori_name = gr.Textbox()

                with gr.Blocks():
                    with gr.Row():
                        file_type = gr.Radio(
                            ["Video", "Audio"],
                            value="Video",
                            label="File Type",
                            interactive=True,
                        )

                    with gr.Row() as video_tab:
                        with gr.Box():
                            with gr.Column():
                                with gr.Row():
                                    url_input = gr.Textbox(
                                        label="Youtbue URL", interactive=True
                                    )

                                with gr.Row():
                                    download_btn = gr.Button(value="Import video")

                                with gr.Row():
                                    video_input = gr.Video(
                                        label="Video File",
                                        interactive=True,
                                        mirror_webcam=False,
                                    )

                    with gr.Row(visible=False) as audio_tab:
                        with gr.Column():
                            audio_input = gr.Audio(
                                label="Audio File",
                                interactive=True,
                                type="filepath",
                            )

                    with gr.Row():
                        source_submit_btn = gr.Button(value="Submit")

                def handle_ydl_download(video_url):
                    ydl_opts = {
                        # "paths": {"home": "mp4/"},
                        "format": "mp4",
                        "outtmpl": "/mp4/%(title)s.%(ext)s",
                        "quiet": True,
                    }

                    with YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=True)
                        filename = ydl.prepare_filename(info)

                        ori_name = os.path.basename(filename)

                    return [filename, ori_name]

                download_btn.click(
                    fn=handle_ydl_download,
                    inputs=url_input,
                    outputs=[video_input, file_ori_name],
                )

                def handle_file_type_change(evt: gr.SelectData):
                    if evt.index == 0:
                        # Video
                        return [
                            gr.update(visible=True),
                            gr.update(visible=False),
                            gr.update(),
                            None,
                        ]
                    elif evt.index == 1:
                        # Audio
                        return [
                            gr.update(visible=False),
                            gr.update(visible=True),
                            None,
                            gr.update(),
                        ]

                file_type.select(
                    handle_file_type_change,
                    None,
                    [video_tab, audio_tab, video_input, audio_input],
                )

                def handle_source_submit(file_type, video, audio):
                    if file_type == "Video":
                        if video is None:
                            return ["", ""]
                        else:
                            return [video, os.path.basename(video)]
                    elif file_type == "Audio":
                        if audio is None:
                            return ["", ""]
                        else:
                            return [audio, os.path.basename(audio)]

                source_submit_btn.click(
                    fn=handle_source_submit,
                    inputs=[file_type, video_input, audio_input],
                    outputs=[file_name, file_ori_name],
                )

            with gr.Tab("Setting", id="setting_tab") as setting_tab:
                with gr.Box():
                    gr.HTML(value="<p><b>Preprocess Setting</b></p>")

                    with gr.Row():
                        with gr.Column():
                            vocal_extracter_checkbox = (
                                gr.Checkbox(
                                    value=True,
                                    label="Vocal extracter",
                                    info="Mute non-vaocal background music",
                                    interactive=True,
                                ),
                            )

                            vocal_extracter_checkbox = (
                                gr.Checkbox(
                                    value=True,
                                    label="Voice activity detection",
                                    info="Should fix the issue of subtitles repeating",
                                    interactive=True,
                                ),
                            )

                with gr.Box():
                    gr.HTML(value="<p><b>Model Setting</b></p>")
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
                    demo_video = gr.Video(
                        label="Demo",
                        interactive=False,
                    )

                with gr.Row():
                    with gr.Accordion("Subtitles", open=False):
                        with gr.Row():
                            srt_download = gr.File(
                                label="srt download", interactive=False
                            )
                            vtt_download = gr.File(
                                label="vtt download", interactive=False
                            )
                            ass_download = gr.File(
                                label="ass download", interactive=False
                            )
                        with gr.Row():
                            demo_subtitle = gr.Markdown()

        # file_type.change(
        #     fn=change_type,
        #     inputs=[file_type],
        #     outputs=[video_input, audio_input, video_url],
        # )

        task_type.change(
            fn=change_task_type,
            inputs=[task_type],
            outputs=[submit_btn],
        )

        # submit_btn.click(
        #     fn=transcribe_submit,
        #     inputs=[
        #         language_input,
        #         precision,
        #         file_type,
        #         video_input,
        #         audio_input,
        #         device,
        #         device,
        #         task_type,
        #         video_name,
        #     ],
        #     outputs=[
        #         progress_txt,
        #         demo_tabs,
        #         srt_download,
        #         vtt_download,
        #         ass_download,
        #         demo_video,
        #         demo_subtitle,
        #     ],
        # )

        def preprocess_submit(preprocess_checked):
            if 0 in preprocess_checked:
                # Vocal extracter
                pass

            if 1 in preprocess_checked:
                # VAD
                pass

            pass

        # def update_origin(path):
        #     print(path)
        #     return path

        # video_input.change(update_origin, inputs=[video_input], outputs=[file_name])
        # audio_input.change(update_origin, inputs=[audio_input], outputs=[file_name])

    return demo


def launch():
    gui().launch()


if __name__ == "__main__":
    print("TEST")
    launch()
else:
    demo = gui()
