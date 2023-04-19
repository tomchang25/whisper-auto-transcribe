import gradio as gr
from src.ui.project_tab import create_project_tab
from src.ui.source_tab import create_source_tab
from src.ui.setting_tab import create_setting_tab
from src.ui.result_tab import create_result_tab


def create_transcribe_tab():
    with gr.Blocks() as demo:
        state = gr.JSON(
            {
                "current_tab": "source_tab",
                "error": "",
            },
            visible=True,
        )
        error = gr.Textbox(label="Error", visible=False)

        with gr.Tabs() as main_tab:
            # Put tab function here
            create_project_tab(state=state)
            create_source_tab(state=state)
            create_setting_tab(state=state)
            create_result_tab(state=state)

            def tab_change(evt: gr.SelectData, state):
                if evt.index == 0:
                    state["current_tab"] = "project_tab"
                elif evt.index == 1:
                    state["current_tab"] = "source_tab"
                elif evt.index == 2:
                    state["current_tab"] = "setting_tab"
                elif evt.index == 3:
                    state["current_tab"] = "result_tab"

                return state

            main_tab.select(
                fn=tab_change,
                inputs=[state],
                outputs=[state],
            )

            def state_change(state):
                main_tab = gr.update(selected=state["current_tab"])

                if state["error"] != "":
                    error = gr.update(value=state["error"], visible=True)
                else:
                    error = gr.update(value=state["error"], visible=False)

                return main_tab, error

            state.change(
                fn=state_change,
                inputs=state,
                outputs=[main_tab, error],
            )

    return demo


# if __name__ == "__main__":
#     demo.launch()
