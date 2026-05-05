from PySide6.QtCore import QObject, Signal, Slot

from services import TranscribeJob, run_job


class JobWorker(QObject):
    progress = Signal(str, float)
    finished = Signal(object)
    failed = Signal(str)

    def __init__(self, job: TranscribeJob) -> None:
        super().__init__()
        self._job = job

    @Slot()
    def run(self) -> None:
        try:
            result = run_job(self._job, progress=self.progress.emit)
        except Exception as e:
            self.failed.emit(str(e))
            return
        self.finished.emit(result)
