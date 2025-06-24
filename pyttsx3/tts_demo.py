import pyttsx3
import time

def main():
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set voice properties
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 25)
    engine.setProperty('volume', 1.0)

    # List available voices
    voices = engine.getProperty('voices')
    print("Available voices:")
    for i, voice in enumerate(voices):
        print(f"{i}: {voice.name} - {voice.id}")
    print()

    # Optional: Choose a specific voice by index
    # engine.setProperty('voice', voices[0].id)

    print("Type 'exit' to quit.")
    while True:
        text = input("Enter text to speak: ")
        if text.strip().lower() == "exit":
            break

        start_time = time.perf_counter()
        engine.say(text)
        engine.runAndWait()
        end_time = time.perf_counter()

        duration = end_time - start_time
        print(f"[Telemetry] Rendered in {duration:.2f} seconds\n")

if __name__ == "__main__":
    main()