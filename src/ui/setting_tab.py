import gradio as gr
from src.utils.constants import (
    LANGUAGE_CODES,
    TRANSCRIBE_MODEL_TYPES,
    MODEL_SIZES,
    DEVICE_TYPES,
    TASK_TYPES,
)
import torch


def handle_setting_save(
    vocal_extracter_checkbox,
    vad_checkbox,
    transcribe_model_input,
    language_input,
    precision_input,
    device_input,
    task_type,
    state,
):
    state["vocal_extracter"] = vocal_extracter_checkbox
    state["vad"] = vad_checkbox
    state["transcribe_model"] = TRANSCRIBE_MODEL_TYPES[transcribe_model_input]
    state["language"] = LANGUAGE_CODES[language_input][0]
    state["model_size"] = MODEL_SIZES[precision_input]
    state["device"] = DEVICE_TYPES[device_input]
    state["task_type"] = TASK_TYPES[task_type]

    state["error"] = ""
    state["current_tab"] = "result_tab"

    return state


def create_setting_tab(state):
    available_device = "GPU" if torch.cuda.is_available() else "CPU"
    with gr.Tab("Setting", id="setting_tab"):
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
                    transcribe_model_input = gr.Dropdown(
                        value="Whisper Timestamps",
                        choices=[
                            "Whisper",
                            "Whisper Timestamps",
                            "Stabilizing Timestamps for Whisper",
                        ],
                        type="index",
                        label="Transcribe model",
                        info="For detailed information, please check the guide",
                        interactive=True,
                    )

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
                        type="index",
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

                setting_save_btn = gr.Button("Save")

    setting_save_btn.click(
        fn=handle_setting_save,
        inputs=[
            vocal_extracter_checkbox,
            vad_checkbox,
            transcribe_model_input,
            language_input,
            precision_input,
            device_input,
            task_type,
            state,
        ],
        outputs=[state],
    )
