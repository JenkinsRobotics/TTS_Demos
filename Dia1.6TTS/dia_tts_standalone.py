"""
Dia TTS Standalone GUI
Author: Jonathan Jenkins
Date: 2025-06-21

Description:
    A simple PySide6 GUI application for generating speech using the Dia-1.6B
    text-to-speech model by Nari Labs. This app supports expressive dialogue 
    synthesis, progress tracking, and local audio playback.

Requirements:
    - Python 3.10+
    - PySide6
    - soundfile
    - sounddevice
    - Dia TTS (https://huggingface.co/nari-labs/Dia-1.6B)

Usage:
    Run the app with:
        python dia_tts_standalone.py

    Enter dialogue in the textbox (supports speaker tags like [S1], [S2])
    and click "Generate Audio" to synthesize. Press "Play Output" to preview.
"""

import sys
import soundfile as sf
import sounddevice as sd
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QLabel, QProgressBar
)
from PySide6.QtCore import Qt, QThread, Signal, QObject
from dia.model import Dia

class TTSWorker(QObject):
    progress = Signal(int)
    finished = Signal()
    error = Signal(str)

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

    def run(self):
        try:
            for i in range(1, 90, 10):
                self.progress.emit(i)

            output = self.model.generate(self.text, use_torch_compile=False)
            sf.write("dia_output.wav", output, 44100)

            self.progress.emit(100)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class DiaTTSApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dia TTS - Standalone Demo")
        self.setMinimumSize(400, 350)

        self.init_ui()
        self.thread = None
        self.worker = None

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Enter dialogue or expressive text:")
        layout.addWidget(self.label)

        self.text_input = QTextEdit()
        layout.addWidget(self.text_input)

        self.speak_button = QPushButton("Generate Audio")
        self.speak_button.clicked.connect(self.start_worker)
        layout.addWidget(self.speak_button)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.play_button = QPushButton("Play Output")
        self.play_button.clicked.connect(self.play_audio)
        self.play_button.setEnabled(False)
        layout.addWidget(self.play_button)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def start_worker(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            self.status_label.setText("Please enter some text.")
            return

        self.status_label.setText("Synthesizing... Please wait.")
        self.play_button.setEnabled(False)
        self.progress.setValue(0)

        self.thread = QThread()
        self.worker = TTSWorker(text)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_finished(self):
        self.status_label.setText("Done! Saved as dia_output.wav.")
        self.play_button.setEnabled(True)

    def on_error(self, message):
        self.status_label.setText(f"Error: {message}")
        self.progress.setValue(0)

    def play_audio(self):
        try:
            data, samplerate = sf.read("dia_output.wav")
            sd.play(data, samplerate)
            self.status_label.setText("Playing audio...")
        except Exception as e:
            self.status_label.setText(f"Playback error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiaTTSApp()
    window.show()
    sys.exit(app.exec())