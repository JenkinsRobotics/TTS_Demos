**Project Name:** Kokoro TTS Standalone GUI Test
**Focus:** Local TTS Evaluation  
**Log:** 002
**Date:** 2025-06-24
**Status:** #Completed

#AIAudio #TTS 

---
### **Current Objective:**

  Evaluate the performance, voice quality, and responsiveness of **Kokoro TTS** in a standalone GUI test app on macOS. Determine suitability for rapid-prototyping AI characters and future streaming or interruptible TTS use in interactive agents.

---
### **Model Information:**

- **Library Name:** Kokoro TTS
- **Version:** 0.1.1 (PyPI package: kokoro)
- **API Used:** KPipeline from kokoro
- **Developer:** Hexgrad (open-source contributor)
- **License:** MIT
- **GitHub:** [https://github.com/hexgrad/kokoro](https://github.com/hexgrad/kokoro)
- **Model Architecture:** FastSpeech-style synthesis (non-autoregressive)
- **Languages Supported:** Primarily English; multilingual in development

---
### **Installation**

```
pip install kokoro sounddevice PySide6
```

---

## **GUI Application Overview**

Built with **PySide6**, the GUI allows users to:

1. Enter free-form dialogue text
2. Select from available voices (e.g., af_heart, am_adam, bf_emma)
3. Generate speech and play back in ~1 second
4. Save audio as WAV
5. Monitor performance with real-time timing logs

### **How It Works:**

- Loads the pipeline via KPipeline(lang_code='a')
- Generates audio using list(pipeline(text, voice=...))
- Concatenates audio chunks and plays via sounddevice

---

### **Sample Input Example:**

```
Welcome back, Captain. I've re-initialized the systems and calibrated the visual sensors.
```

- Rendering Time: ~1.1s on M2 Max (macOS)
- Output Quality: Natural, friendly voice; medium prosody

---

### **Usage Instructions:**

```
python kokoro_gui.py
```

- Type text and choose voice
- Press “🔊 Speak” to synthesize and play
- Press “💾 Save WAV” to export

---

### **Future Plans:**

- Integrate audio playback monitoring / interrupt logic
- Add real-time generation stream support (when available)
- Enable in-GUI multilingual switching
- Explore speaker verification & echo cancellation pairing

---

**Log Status:** Completed

**Notes:** Excellent for medium-latency voice responses; suitable for offline agent personas. Cannot yet handle real-time interruptions or streaming.

---
