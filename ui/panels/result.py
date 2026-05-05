from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
)

from services import JobResult, save_subtitles


class ResultPanel(QGroupBox):
    def __init__(self, parent=None) -> None:
        super().__init__("Result", parent)
        self._result: Optional[JobResult] = None

        layout = QVBoxLayout(self)

        self._progress = QProgressBar()
        self._progress.setRange(0, 100)
        self._progress.setFormat("%p%")
        layout.addWidget(self._progress)

        self._preview = QPlainTextEdit()
        self._preview.setReadOnly(True)
        self._preview.setPlaceholderText("Subtitle text will appear here after transcription.")
        layout.addWidget(self._preview, 1)

        export_row = QHBoxLayout()
        for fmt in ("srt", "vtt", "ass", "json"):
            btn = QPushButton(f"Save {fmt.upper()}")
            btn.clicked.connect(lambda _checked=False, f=fmt: self._export(f))
            export_row.addWidget(btn)
        layout.addLayout(export_row)

    def set_progress(self, stage: str, fraction: float) -> None:
        self._progress.setFormat(f"{stage}: %p%")
        self._progress.setValue(int(fraction * 100))

    def set_result(self, result: JobResult) -> None:
        self._result = result
        text = "\n".join(seg.text.strip() for seg in result.segments)
        self._preview.setPlainText(text)
        self._progress.setFormat("done: %p%")
        self._progress.setValue(100)

    def reset(self) -> None:
        self._result = None
        self._preview.clear()
        self._progress.setFormat("%p%")
        self._progress.setValue(0)

    def _export(self, fmt: str) -> None:
        if self._result is None:
            QMessageBox.information(self, "No result", "Run a transcription first.")
            return
        default = self._result.output_files.get("srt")
        default_name = (Path(default).with_suffix(f".{fmt}").name if default else f"subtitles.{fmt}")
        path_str, _ = QFileDialog.getSaveFileName(
            self, f"Save {fmt.upper()}", default_name, f"{fmt.upper()} (*.{fmt})"
        )
        if not path_str:
            return
        try:
            save_subtitles(self._result.segments, path_str, fmt)
        except Exception as e:
            QMessageBox.critical(self, "Save failed", str(e))
