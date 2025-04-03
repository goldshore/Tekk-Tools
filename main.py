import os
import whisper
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def transcribe_audio(audio_path):
    """Transcribes audio using the Whisper model."""
    model_name = os.getenv("WHISPER_MODEL", "base")
    model = whisper.load_model(model_name)

    try:
        result = model.transcribe(audio_path)
        return result['text']
    except RuntimeError as e:
        print(f"Error during transcription: {e}")
        return None

def main():
    """Main function to transcribe an audio file."""
    audio_path = os.getenv(
        "AUDIO_PATH",
        "/workspaces/Tekk-Tools/tekk-tools/arthurgpt/audio_upload/uploads/sample_audio.wav"
    )

    if not os.path.isfile(audio_path):
        print(f"Error: Audio file not found at {audio_path}")
        return

    transcription = transcribe_audio(audio_path)
    if transcription:
        print("Transcription:", transcription)
    else:
        print("Failed to transcribe the audio.")

if __name__ == "__main__":
    main()