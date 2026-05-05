import tempfile
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from services.youtube import download


class SourcePanel(QGroupBox):
    source_changed = Signal(object)

    def __init__(self, parent=None) -> None:
        super().__init__("Source", parent)
        self._selected: Optional[Path] = None

        layout = QVBoxLayout(self)

        file_row = QHBoxLayout()
        self._path_label = QLabel("No file selected")
        browse_btn = QPushButton("Browse…")
        browse_btn.clicked.connect(self._browse)
        file_row.addWidget(self._path_label, 1)
        file_row.addWidget(browse_btn)
        layout.addLayout(file_row)

        url_row = QHBoxLayout()
        self._url_input = QLineEdit()
        self._url_input.setPlaceholderText("YouTube URL…")
        import_btn = QPushButton("Import")
        import_btn.clicked.connect(self._import_url)
        url_row.addWidget(self._url_input, 1)
        url_row.addWidget(import_btn)
        layout.addLayout(url_row)

    @property
    def selected_path(self) -> Optional[Path]:
        return self._selected

    def _set_selected(self, path: Path) -> None:
        self._selected = path
        self._path_label.setText(str(path))
        self.source_changed.emit(path)

    def _browse(self) -> None:
        path_str, _ = QFileDialog.getOpenFileName(
            self,
            "Select media file",
            "",
            "Media Files (*.mp4 *.mov *.mkv *.avi *.webm *.mp3 *.wav *.m4a *.flac);;All Files (*)",
        )
        if path_str:
            self._set_selected(Path(path_str))

    def _import_url(self) -> None:
        url = self._url_input.text().strip()
        if not url:
            return
        dest = Path(tempfile.gettempdir()) / "whisper-auto-transcribe" / "downloads"
        try:
            path = download(url, dest)
        except Exception as e:
            QMessageBox.critical(self, "Download failed", str(e))
            return
        self._set_selected(path)
