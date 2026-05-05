from pathlib import Path

from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QRadioButton,
    QWidget,
)

from services import TranscribeJob
from src.utils.constants import LANGUAGE_CODES, MODEL_SIZES


def _has_cuda() -> bool:
    try:
        import torch
        return bool(torch.cuda.is_available())
    except Exception:
        return False


class SettingsPanel(QGroupBox):
    def __init__(self, parent=None) -> None:
        super().__init__("Settings", parent)
        layout = QFormLayout(self)

        self._model = QComboBox()
        self._model.addItems(MODEL_SIZES)
        self._model.setCurrentText("medium")
        layout.addRow("Model size", self._model)

        self._language = QComboBox()
        for code, name in LANGUAGE_CODES:
            self._language.addItem(name, code)
        layout.addRow("Language", self._language)

        device_row = QWidget()
        device_layout = QHBoxLayout(device_row)
        device_layout.setContentsMargins(0, 0, 0, 0)
        self._device_group = QButtonGroup(self)
        self._cpu_btn = QRadioButton("CPU")
        self._gpu_btn = QRadioButton("GPU")
        self._cpu_btn.setChecked(True)
        if not _has_cuda():
            self._gpu_btn.setEnabled(False)
            self._gpu_btn.setToolTip("CUDA not available")
        self._device_group.addButton(self._cpu_btn)
        self._device_group.addButton(self._gpu_btn)
        device_layout.addWidget(self._cpu_btn)
        device_layout.addWidget(self._gpu_btn)
        device_layout.addStretch(1)
        layout.addRow("Device", device_row)

        task_row = QWidget()
        task_layout = QHBoxLayout(task_row)
        task_layout.setContentsMargins(0, 0, 0, 0)
        self._task_group = QButtonGroup(self)
        self._transcribe_btn = QRadioButton("Transcribe")
        self._translate_btn = QRadioButton("Translate")
        self._transcribe_btn.setChecked(True)
        self._task_group.addButton(self._transcribe_btn)
        self._task_group.addButton(self._translate_btn)
        task_layout.addWidget(self._transcribe_btn)
        task_layout.addWidget(self._translate_btn)
        task_layout.addStretch(1)
        layout.addRow("Task", task_row)

        self._vocal = QCheckBox("Run vocal extraction (demucs) before transcribe")
        self._vocal.setChecked(True)
        layout.addRow(self._vocal)

    def build_job(self, input_path: Path, output_path: Path) -> TranscribeJob:
        lang_code = self._language.currentData()
        return TranscribeJob(
            input_path=input_path,
            output_path=output_path,
            language=None if lang_code == "auto" else lang_code,
            model_size=self._model.currentText(),
            device="cuda" if self._gpu_btn.isChecked() else "cpu",
            task="translate" if self._translate_btn.isChecked() else "transcribe",
            vocal_extraction=self._vocal.isChecked(),
            formats=("srt",),
        )
