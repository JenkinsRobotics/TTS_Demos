from kokoro import KPipeline
import sounddevice as sd
import numpy as np
import time

def main():
    print("Kokoro TTS (CLI) ready.")
    print("Type 'exit' to quit.")

    # Initialize Kokoro TTS pipeline for English
    pipeline = KPipeline(lang_code='a')
    default_voice = "af_heart"  # You can change this or add a voice picker

    while True:
        text = input("Enter text to speak: ")
        if text.strip().lower() == "exit":
            break

        try:
            start_time = time.perf_counter()

            # Run pipeline and collect audio chunks
            results = list(pipeline(text, voice=default_voice))
            audio_chunks = [r.audio for r in results]
            audio = np.concatenate(audio_chunks)

            elapsed = time.perf_counter() - start_time
            print(f"[Telemetry] Rendered in {elapsed:.2f} seconds")

            # Playback
            sd.play(audio, samplerate=24000)
            sd.wait()
        except Exception as e:
            print("❌ Error during synthesis:", e)

if __name__ == "__main__":
    main()