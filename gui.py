from src import transcribe_gui


def gui():
    return transcribe_gui.create_transcribe_tab()


if __name__ == "__main__":
    gui().launch()
else:
    demo = gui()
