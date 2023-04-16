import gradio as gr
from src.utils import processing_utils


def create_test_compress_tab():
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                file_type = gr.Radio(
                    ["Video", "Audio"],
                    value="Video",
                    label="File Type",
                    interactive=True,
                )
                video = gr.Video()
                audio = gr.Audio(visible=False)
                btn = gr.Button()
            with gr.Column():
                file = gr.File()

            def handle_file_type_change(evt: gr.SelectData):
                if evt.index == 0:
                    # Video
                    return [gr.update(visible=True), gr.update(visible=False)]
                elif evt.index == 1:
                    # Audio
                    return [gr.update(visible=False), gr.update(visible=True)]

            file_type.select(
                handle_file_type_change,
                None,
                [video, audio],
            )

        def handle_btn_submit(file_type, video, audio):
            if file_type == "Video":
                audio_data = processing_utils.audio_from_file(video)
            elif file_type == "Audio":
                audio_data = processing_utils.audio_from_file(audio)

            audio_data.export("tmp/test.mp3", format="mp3", bitrate="96k")

            return "tmp/test.mp3"

        btn.click(
            fn=handle_btn_submit,
            inputs=[file_type, video, audio],
            outputs=[file],
        )

    return demo


demo = create_test_compress_tab()
