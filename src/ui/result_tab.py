import gradio as gr
from src.utils.constants import TEMPDIR
from src.utils.task import start_task
import pysubs2
from pathlib import Path


def handle_update_subtitle_output(subtitle_output, state):
    state["subtitle_output"] = subtitle_output
    return state


def handle_video_demo(subtitle_output, state):
    return gr.update(value=(state["source_filename"], subtitle_output))


def handle_subtitle_format(subtitle_output):
    # Generate vtt, ass from srt

    subtitle = pysubs2.load(subtitle_output, encoding="utf-8")

    vtt_file_path = Path(subtitle_output).with_suffix(".vtt")
    subtitle.save(vtt_file_path)

    ass_file_path = Path(subtitle_output).with_suffix(".ass")
    subtitle.save(ass_file_path)

    json_file_path = Path(subtitle_output).with_suffix(".json")
    subtitle.save(json_file_path)

    fake_subtitle_dataframe = "```" + subtitle.to_string("srt") + "```"

    return [
        subtitle_output,
        vtt_file_path,
        ass_file_path,
        json_file_path,
        fake_subtitle_dataframe,
    ]


def handle_start_work(state):
    media = state["source_filename"]

    subtitle_output = start_task(
        media,
        subtitle=None,
        ve=state["vocal_extracter"],
        vad=state["vad"],
        transcribe_model=state["transcribe_model"],
        language=state["language"],
        model_size=state["model_size"],
        task_type=state["task_type"],
        device=state["device"],
        delete_tempfile=True,
    )

    state["error"] = ""
    state["current_tab"] = "result_tab"

    return subtitle_output, state


def create_result_tab(state):
    with gr.Tab("Result", id="result_tab"):
        subtitle_output = gr.Textbox(visible=True)
        with gr.Column():
            start_btn = gr.Button("Start")

            video_demo = gr.Video(
                label="Demo",
                interactive=False,
            )

            with gr.Accordion("Subtitle", open=False):
                with gr.Column():
                    with gr.Row():
                        srt_download = gr.File(label="srt", interactive=False)
                        vtt_download = gr.File(label="vtt", interactive=False)
                        ass_download = gr.File(label="ass", interactive=False)
                        json_file_path = gr.File(label="json", interactive=False)

                    subtitle_dataframe = gr.Markdown()

    start_btn.click(
        fn=handle_start_work,
        inputs=[state],
        outputs=[subtitle_output, state],
    )

    subtitle_output.change(
        fn=handle_subtitle_format,
        inputs=[subtitle_output],
        outputs=[
            srt_download,
            vtt_download,
            ass_download,
            json_file_path,
            subtitle_dataframe,
        ],
    )

    subtitle_output.change(
        fn=handle_video_demo,
        inputs=[subtitle_output, state],
        outputs=[video_demo],
    )

    subtitle_output.change(
        fn=handle_update_subtitle_output,
        inputs=[subtitle_output, state],
        outputs=[state],
    )
