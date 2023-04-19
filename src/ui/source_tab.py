import gradio as gr
from yt_dlp import YoutubeDL
from pydub import AudioSegment
from src.utils.constants import TEMPDIR
from pathlib import Path


def handle_ydl_download(video_url, state):
    ydl_opts = {
        "format": "mp4",
        "outtmpl": "/mp4/%(title)s.%(ext)s",
        "quiet": True,
    }

    if video_url.strip() == "":
        state["error"] = f"Invalid value for parameter `Youtbue URL `: {video_url}."
        return [None, None, state]

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        download_filename = ydl.prepare_filename(info)

    audio_filename = TEMPDIR / Path("youtube_audio.wav")
    AudioSegment.from_file(download_filename).export(audio_filename)

    state["error"] = ""

    return download_filename, audio_filename, state


def handle_file_type_change(evt: gr.SelectData):
    if evt.index == 0:
        # Video
        return [
            gr.update(visible=True),
            gr.update(visible=False),
        ]
    elif evt.index == 1:
        # Audio
        return [
            gr.update(visible=False),
            gr.update(visible=True),
        ]


def handle_source_save(file_type, video, audio, state):
    if file_type == "Video":
        if video is None:
            state["error"] = f"Invalid value for parameter `Video`: {video}."
            return state

        source_filename = video
    elif file_type == "Audio":
        if audio is None:
            state["error"] = f"Invalid value for parameter `Audio`: {audio}."
            return state

        source_filename = audio

    state["source_filename"] = source_filename

    state["error"] = ""
    state["current_tab"] = "setting_tab"

    return state


def create_source_tab(state):
    with gr.Tab("Source", id="source_tab"):
        with gr.Column():
            file_type = gr.Radio(
                ["Video", "Audio"],
                value="Video",
                label="File type",
                interactive=True,
            )

            with gr.Box():
                with gr.Column():
                    url_input = gr.Textbox(label="Youtbue URL", interactive=True)
                    download_btn = gr.Button(value="Download")

            with gr.Column():
                video_input = gr.Video(
                    label="Video File",
                    interactive=True,
                    mirror_webcam=False,
                )

                audio_input = gr.Audio(
                    label="Audio File",
                    interactive=True,
                    visible=False,
                    type="filepath",
                )

            source_save_btn = gr.Button(value="Save")

    download_btn.click(
        fn=handle_ydl_download,
        inputs=[url_input, state],
        outputs=[video_input, audio_input, state],
    )

    file_type.select(
        handle_file_type_change,
        None,
        [video_input, audio_input],
    )

    source_save_btn.click(
        fn=handle_source_save,
        inputs=[file_type, video_input, audio_input, state],
        outputs=[state],
    )
