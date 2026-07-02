from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from omnistem import __version__


def main() -> None:
    try:
        from PySide6.QtCore import QThread, Signal
        from PySide6.QtWidgets import (
            QApplication,
            QCheckBox,
            QComboBox,
            QFileDialog,
            QFormLayout,
            QHBoxLayout,
            QLabel,
            QLineEdit,
            QMainWindow,
            QMessageBox,
            QPlainTextEdit,
            QPushButton,
            QVBoxLayout,
            QWidget,
        )
    except ImportError as exc:
        raise RuntimeError('Install desktop support with: pip install "omnistem[desktop]"') from exc

    from omnistem.core.orchestrator import Orchestrator
    from omnistem.core.types import SeparationJob
    from omnistem.engines.registry import engine_registry

    class Worker(QThread):
        line = Signal(str)
        finished_result = Signal(object)
        failed = Signal(str)

        def __init__(self, job: SeparationJob) -> None:
            super().__init__()
            self.job = job

        def run(self) -> None:
            try:
                result = asyncio.run(Orchestrator().run(self.job, on_line=self.line.emit))
                self.finished_result.emit(result)
            except Exception as exc:
                self.failed.emit(str(exc))

    class Window(QMainWindow):
        def __init__(self) -> None:
            super().__init__()
            self.worker = None
            self.setWindowTitle(f"OmniStem God Mode {__version__}")
            self.resize(900, 620)
            central = QWidget()
            layout = QVBoxLayout(central)
            form = QFormLayout()

            self.input_edit = QLineEdit()
            input_row = QHBoxLayout()
            input_row.addWidget(self.input_edit)
            input_button = QPushButton("Browse")
            input_button.clicked.connect(self.pick_input)
            input_row.addWidget(input_button)
            form.addRow("Audio file", input_row)

            self.output_edit = QLineEdit(str(Path("outputs").resolve()))
            output_row = QHBoxLayout()
            output_row.addWidget(self.output_edit)
            output_button = QPushButton("Browse")
            output_button.clicked.connect(self.pick_output)
            output_row.addWidget(output_button)
            form.addRow("Output folder", output_row)

            self.engine_combo = QComboBox()
            self.engine_combo.addItems(sorted(engine_registry()))
            form.addRow("Engine", self.engine_combo)

            self.model_edit = QLineEdit()
            self.model_edit.setPlaceholderText("Optional native model name or checkpoint filename")
            form.addRow("Model", self.model_edit)

            self.stems_edit = QLineEdit("vocals,instrumental")
            form.addRow("Stems", self.stems_edit)

            self.overwrite_check = QCheckBox("Allow non-empty output directory")
            form.addRow("Overwrite", self.overwrite_check)
            layout.addLayout(form)

            self.status_label = QLabel("Ready")
            layout.addWidget(self.status_label)
            self.log = QPlainTextEdit()
            self.log.setReadOnly(True)
            layout.addWidget(self.log, 1)

            self.start_button = QPushButton("Separate")
            self.start_button.clicked.connect(self.start_job)
            layout.addWidget(self.start_button)
            self.setCentralWidget(central)

        def pick_input(self) -> None:
            filename, _ = QFileDialog.getOpenFileName(self, "Select audio")
            if filename:
                self.input_edit.setText(filename)

        def pick_output(self) -> None:
            directory = QFileDialog.getExistingDirectory(self, "Select output directory")
            if directory:
                self.output_edit.setText(directory)

        def start_job(self) -> None:
            path = Path(self.input_edit.text())
            if not path.is_file():
                QMessageBox.warning(self, "Invalid input", "Select an existing audio file.")
                return
            job = SeparationJob(
                input_file=path,
                output_dir=Path(self.output_edit.text()),
                engine=self.engine_combo.currentText(),
                model=self.model_edit.text().strip() or None,
                stems=tuple(
                    part.strip() for part in self.stems_edit.text().split(",") if part.strip()
                ),
                overwrite=self.overwrite_check.isChecked(),
            )
            self.log.clear()
            self.start_button.setEnabled(False)
            self.status_label.setText("Processing")
            self.worker = Worker(job)
            self.worker.line.connect(self.log.appendPlainText)
            self.worker.failed.connect(self.on_failed)
            self.worker.finished_result.connect(self.on_finished)
            self.worker.start()

        def on_failed(self, message: str) -> None:
            self.start_button.setEnabled(True)
            self.status_label.setText("Failed")
            QMessageBox.critical(self, "OmniStem error", message)

        def on_finished(self, result: object) -> None:
            self.start_button.setEnabled(True)
            ok = bool(getattr(result, "ok", False))
            self.status_label.setText("Completed" if ok else "Failed")
            manifest = getattr(result, "manifest_path", "")
            self.log.appendPlainText(f"Manifest: {manifest}")

    application = QApplication(sys.argv)
    application.setStyle("Fusion")
    window = Window()
    window.show()
    raise SystemExit(application.exec())


if __name__ == "__main__":
    main()
