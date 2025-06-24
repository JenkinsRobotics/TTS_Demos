**Project Name:** Dia TTS Standalone GUI Test  
**Focus:** Local TTS Evaluation  
**Log:** 001  
**Date:** 2025-06-21  
**Status:** #Completed

#AIAudio #TTS 

**Current Objective:**  
To evaluate the Nari Labs **Dia-1.6B** open-source TTS model through a standalone GUI test application. The goal is to understand its expressive dialogue capabilities, assess performance on macOS, and establish a flexible base for future multi-agent AI voice integration.

---

### Model Information:

- **Model Name:** Dia
- **Model Version:** 1.6B
- **Developer:** Nari Labs
- **License:** Apache 2.0 (Open Source)
- **HuggingFace Page:** [https://huggingface.co/nari-labs/Dia-1.6B](https://huggingface.co/nari-labs/Dia-1.6B)
- **GitHub Repo:** [https://github.com/nari-labs/dia](https://github.com/nari-labs/dia)

---
## Installation

### Requirements:

- Python 3.10+
- macOS with MPS backend (or CUDA on Linux/Windows)

### Install Commands:

```bash
pip install git+https://github.com/nari-labs/dia.git
pip install PySide6 soundfile sounddevice
```

---
## Demo Application Overview

A simple GUI was developed using **PySide6** that allows the user to:

1. Enter expressive text input (multi-character dialogue, emotional cues)
2. Run inference using Dia-1.6B locally
3. Save output as a WAV file
4. Playback output using the integrated play button
5. Track progress of synthesis with a real-time progress bar

### How It Works:

- Model loads with `compute_dtype="float16"`
- Uses `model.generate(text)` for waveform synthesis
- Output saved to `dia_output.wav`

### Sample Input Example:

```text
[S1] Oh fire! Oh my goodness! What's the procedure? What do we do people? The smoke could be coming through an air duct!  
[S2] Oh my god! Okay.. it's happening. Everybody stay calm!  
[S1] What's the procedure...  
[S2] Everybody stay fucking calm!!!... Everybody fucking calm down!!!!!  
[S1] No! No! If you touch the handle, if it's hot there might be a fire down the hallway!  
```

Dia automatically parses the `[S1]`, `[S2]` speaker tags and adjusts cadence, tone, and pause timings.

---

## Usage Instructions

1. Launch the app:

```bash
python dia_tts_standalone.py
```

2. Paste expressive text into the textbox.
3. Press **Generate Audio**.
4. Audio will be saved as `dia_output.wav`.
5. Press **Play Output** to listen.

---

## Next Steps / Future Additions

- Add audio playback directly in GUI (✅ Done)
- Run multiple speaker voices in parallel threads
- Support real-time streaming output
- Fine-tune or tag emotional states like (laughs)` or `(angry)`

---

**Log Status:** Completed

**Final Notes:**

Overall, the Dia TTS GUI app works well and demonstrates expressive voice synthesis. However, due to its non-real-time nature and full-sentence synthesis delay, it does not meet the latency requirements for our humanoid robot. We will explore alternate TTS solutions that support real-time interaction and streaming capability.