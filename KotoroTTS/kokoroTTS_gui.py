"""
Kokoro TTS GUI (Standalone) - macOS Compatible
Author: Jonathan Jenkins
Date: 2025-06-17
Description:
    A simple Python GUI to synthesize speech from text using the Kokoro TTS engine 
    (installed via PyPI). Built using PySide6 for cross-platform GUI and sounddevice 
    for audio playback.

Requirements:
    - Python 3.10 or 3.11 (recommended, avoid 3.12 for now)
    - Apple Silicon or Intel Mac (M1/M2/M3 works best with MPS)
    - Internet connection for model downloads (first-time run)

Install Instructions (Terminal):
    # Step 1: Create a virtual environment (optional but recommended)
    python3 -m venv kokoro_env
    source kokoro_env/bin/activate

    # Step 2: Install dependencies
    pip install kokoro sounddevice scipy PySide6

    # Step 3: Run the app with GPU acceleration (for M1/M2/M3 Macs)
    PYTORCH_ENABLE_MPS_FALLBACK=1 python kokoro_gui.py
    
    
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Usage:
    - Type your desired phrase in the text box.
    - Select a voice from the dropdown.
    - Click 🔊 "Speak" to generate and play audio.
    - Click 💾 "Save WAV" to export the result.

Voice Codes (examples):
    - af_heart      : American Female (neutral)
    - af_nicole     : American Female (warm)
    - am_adam       : American Male
    - bf_emma       : British Female
    - bm_george     : British Male

Notes:
    - Uses KPipeline API from `kokoro` PyPI package.
    - Audio is generated in ~1s, streamed internally.
    - GUI is async-friendly but uses blocking playback for simplicity.

"""
# Monkeypatch espeakng_loader to avoid missing phontab error
import os
os.environ["ESPEAKNG_DATA_PATH"] = "/opt/homebrew/share/espeak-ng-data"  # ✅ fixes phontab error

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit,
    QLabel, QComboBox, QFileDialog
)
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import sys
import torch
from kokoro import KPipeline

import json

def load_voice_list(json_path="voices.json"):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
        # Place favorites first, then the rest (no duplicates)
        favorites = data.get("favorites", [])
        all_voices = data.get("all_voices", [])
        ordered_voices = favorites + [v for v in all_voices if v not in favorites]
        return ordered_voices
    except Exception as e:
        print("⚠️ Failed to load voice list:", e)
        return [
            "af_heart", "af_nicole", "am_adam", "bf_emma", "bm_george"
        ]  # fallback

class KokoroTTSApp(QWidget):
    def __init__(self):
        super().__init__()
        print("Using MPS:", torch.backends.mps.is_available())
        print("MPS fallback:", torch.backends.mps.is_built())



        self.setWindowTitle("Kokoro TTS GUI")
        self.resize(400, 300)

        # Preload pipeline for American English (lang_code='a')
        self.pipeline = KPipeline(lang_code='a')
        self.last_audio = None

        # Build GUI
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter text:"))
        self.text_input = QTextEdit()
        layout.addWidget(self.text_input)

        layout.addWidget(QLabel("Choose voice:"))
        self.voice_dropdown = QComboBox()
        self.voice_dropdown.addItems(load_voice_list())
        layout.addWidget(self.voice_dropdown)

        self.speak_button = QPushButton("🔊 Speak")
        self.save_button = QPushButton("💾 Save WAV")
        layout.addWidget(self.speak_button)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.speak_button.clicked.connect(self.speak_text)
        self.save_button.clicked.connect(self.save_audio)

    def speak_text(self):
        text = self.text_input.toPlainText().strip()
        voice = self.voice_dropdown.currentText()
        if not text:
            return

        try:
            import time
            start = time.time()

            results = list(self.pipeline(text, voice=voice))
            audio_chunks = [r.audio for r in results]  # ✅ correct way
            audio = np.concatenate(audio_chunks)

            elapsed = time.time() - start
            print(f"⏱️ Generation time: {elapsed:.2f} seconds")

            self.last_audio = audio
            sd.play(audio, 24000)

        except Exception as e:
            print("TTS error:", e)

    def save_audio(self):
        if self.last_audio is None:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "output.wav", "WAV files (*.wav)")
        if path:
            write(path, 24000, np.int16(self.last_audio * 32767))

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = KokoroTTSApp()
    window.show()
    sys.exit(app.exec())