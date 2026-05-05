import tempfile
from pathlib import Path

from PySide6.QtCore import QThread, Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from services import JobResult
from ui.panels.result import ResultPanel
from ui.panels.settings import SettingsPanel
from ui.panels.source import SourcePanel
from ui.worker import JobWorker


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Whisper Auto Transcribe")
        self.resize(960, 720)

        self._thread: QThread | None = None
        self._worker: JobWorker | None = None

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        splitter = QSplitter(Qt.Orientation.Vertical)
        self._source = SourcePanel()
        self._settings = SettingsPanel()
        self._result = ResultPanel()
        splitter.addWidget(self._source)
        splitter.addWidget(self._settings)
        splitter.addWidget(self._result)
        splitter.setStretchFactor(2, 1)
        root.addWidget(splitter, 1)

        action_row = QHBoxLayout()
        self._start_btn = QPushButton("Start transcription")
        self._start_btn.clicked.connect(self._start_job)
        action_row.addStretch(1)
        action_row.addWidget(self._start_btn)
        root.addLayout(action_row)

    def _start_job(self) -> None:
        if self._thread is not None:
            return

        input_path = self._source.selected_path
        if input_path is None:
            QMessageBox.information(self, "No source", "Select a media file first.")
            return

        out_dir = Path(tempfile.gettempdir()) / "whisper-auto-transcribe" / "output"
        out_dir.mkdir(parents=True, exist_ok=True)
        output_path = out_dir / input_path.stem

        job = self._settings.build_job(input_path=input_path, output_path=output_path)

        self._result.reset()
        self._start_btn.setEnabled(False)

        self._thread = QThread(self)
        self._worker = JobWorker(job)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._result.set_progress)
        self._worker.finished.connect(self._on_finished)
        self._worker.failed.connect(self._on_failed)
        self._thread.start()

    def _cleanup_thread(self) -> None:
        if self._thread is not None:
            self._thread.quit()
            self._thread.wait()
            self._thread.deleteLater()
            self._thread = None
        if self._worker is not None:
            self._worker.deleteLater()
            self._worker = None
        self._start_btn.setEnabled(True)

    def _on_finished(self, result: JobResult) -> None:
        self._result.set_result(result)
        self._cleanup_thread()

    def _on_failed(self, message: str) -> None:
        QMessageBox.critical(self, "Transcription failed", message)
        self._cleanup_thread()
