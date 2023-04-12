import gradio as gr
from yt_dlp import YoutubeDL

from pathlib import Path
import torch

from utils.constants import LANGUAGE_CODES

available_device = "GPU" if torch.cuda.is_available() else "CPU"


def create_source_tab():
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
                        url_input = gr.Textbox(label="Youtbue URL", interactive=True)
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
            "format": "mp4",
            "outtmpl": "/mp4/%(title)s.%(ext)s",
            "quiet": True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            download_file_path = ydl.prepare_filename(info)

        return download_file_path

    download_btn.click(fn=handle_ydl_download, inputs=url_input, outputs=video_input)

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
            file = video
        elif file_type == "Audio":
            file = audio

        return [file, Path(file).name] if file else [None, None]

    source_submit_btn.click(
        fn=handle_source_submit,
        inputs=[file_type, video_input, audio_input],
        outputs=[file_name, file_ori_name],
    )

    return [file_name, file_ori_name, source_submit_btn]


def create_setting_tab():
    with gr.Box():
        gr.HTML(value="<p><b>Preprocess Setting</b></p>")

        with gr.Row():
            with gr.Column():
                vocal_extracter_checkbox = gr.Checkbox(
                    value=True,
                    label="Vocal extracter",
                    info="Mute non-vaocal background music",
                    interactive=True,
                )

                vad_checkbox = gr.Checkbox(
                    value=True,
                    label="Voice activity detection",
                    info="Should fix the issue of subtitle repetition",
                    interactive=True,
                )

    with gr.Box():
        gr.HTML(value="<p><b>Model Setting</b></p>")
        with gr.Column():
            with gr.Row():
                language_input = gr.Dropdown(
                    value="Auto",
                    choices=[x[1] for x in LANGUAGE_CODES],
                    type="index",
                    label="Language",
                    info="Select the desired video language to improve speed.",
                    interactive=True,
                )

                precision_input = gr.Dropdown(
                    choices=[
                        ("Low"),
                        ("Medium-Low"),
                        ("Medium"),
                        ("Medium-High (Recommend)"),
                        ("High"),
                    ],
                    type="index",
                    value="Medium-High (Recommend)",
                    label="Precision",
                    info="Higher precision requires more time.",
                    interactive=True,
                )

            with gr.Row():
                device_input = gr.Radio(
                    value=available_device,
                    choices=["CPU", "GPU"],
                    label="Device",
                    info="Please note that increasing the precision will require more time to process. If you require GPU support, please visit our GitHub page.",
                    interactive=(available_device == "GPU"),
                )

                task_type = gr.Radio(
                    choices=["Transcribe", "Translate"],
                    type="index",
                    value="Transcribe",
                    label="Task",
                    info="The built-in translation feature is inferior. It is recommended to use professional translation tools for higher precision translations",
                    interactive=True,
                )

            setting_submit_btn = gr.Button("Initiate Job")

    return [
        vocal_extracter_checkbox,
        vad_checkbox,
        language_input,
        precision_input,
        device_input,
        task_type,
        setting_submit_btn,
    ]


def create_result_tab():
    with gr.Box():
        with gr.Row():
            video_demo = gr.Video(
                label="Demo",
                interactive=False,
            )

        with gr.Row():
            with gr.Accordion("Subtitles", open=False):
                with gr.Column():
                    subtitle_file_path = gr.Text(label="Subtitle", interactive=False)

                with gr.Row():
                    srt_download = gr.File(label="srt download", interactive=False)
                    vtt_download = gr.File(label="vtt download", interactive=False)
                    ass_download = gr.File(label="ass download", interactive=False)
                with gr.Row():
                    demo_subtitle = gr.Markdown()

    return video_demo, subtitle_file_path


with gr.Blocks() as demo:
    with gr.Tabs() as main_tab:
        with gr.Tab("Source", id="source_tab"):
            (file_name, file_ori_name, source_submit_btn) = create_source_tab()
        with gr.Tab("Setting", id="setting_tab"):
            (
                vocal_extracter_checkbox,
                vad_checkbox,
                language_input,
                precision_input,
                device_input,
                task_type,
                setting_submit_btn,
            ) = create_setting_tab()
        with gr.Tab("Result", id="result_tab"):
            video_demo, subtitle_file_path = create_result_tab()

        source_submit_btn.click(
            fn=lambda: gr.update(selected="setting_tab"),
            inputs=None,
            outputs=main_tab,
        )

        setting_submit_btn.click(
            fn=lambda: gr.update(selected="result_tab"),
            inputs=None,
            outputs=main_tab,
        )

        def handle_form_submit(
            file_name,
            file_ori_name,
            vocal_extracter_checkbox,
            vad_checkbox,
            language_input,
            precision_input,
            device_input,
            task_type,
        ):
            # Perform subtitle transcription

            return [
                gr.update(value=file_name),
                gr.update(value=Path(file_ori_name).with_suffix(".srt")),
            ]

        setting_submit_btn.click(
            fn=handle_form_submit,
            inputs=[
                file_name,
                file_ori_name,
                vocal_extracter_checkbox,
                vad_checkbox,
                language_input,
                precision_input,
                device_input,
                task_type,
            ],
            outputs=[video_demo, subtitle_file_path],
        )

if __name__ == "__main__":
    demo.launch()
