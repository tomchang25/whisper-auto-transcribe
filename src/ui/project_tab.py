import gradio as gr
from src.utils.constants import TEMPDIR


def handle_classic_enter(state):
    state["project_mode"] = "classic"

    state["error"] = ""
    state["current_tab"] = "source_tab"

    return state


def handle_project_enter(project_name_input, state):
    # TODO: Check project name duplicate
    if project_name_input == "":
        state["error"] = f"Invalid value for parameter `Project name`: {project_name_input}."
        return state

    state["project_mode"] = "project"
    state["project_name"] = project_name_input

    state["error"] = ""
    state["current_tab"] = "source_tab"

    return state


def create_project_tab(state):
    with gr.Tab("Project", id="project_tab"):
        with gr.Column():
            with gr.Box() as classic_box:
                with gr.Column():
                    classic_enter_btn = gr.Button(value="Enter Classic Mode")

            with gr.Box() as project_box:
                with gr.Column():
                    project_name_input = gr.Textbox(label="Project Name", interactive=True)
                    project_enter_btn = gr.Button(value="Enter Project Mode")

    classic_enter_btn.click(
        fn=handle_classic_enter,
        inputs=[state],
        outputs=[state],
    )

    project_enter_btn.click(
        fn=handle_project_enter,
        inputs=[project_name_input, state],
        outputs=[state],
    )
