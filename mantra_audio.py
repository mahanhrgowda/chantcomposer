
# mantra_audio.py

from io import BytesIO
from pydub.generators import Sine

def synthesize_audio(text):
    duration = len(text) * 100  # 100 ms per character
    audio = Sine(440).to_audio_segment(duration=duration)
    buf = BytesIO()
    audio.export(buf, format="wav")
    return buf.getvalue()

def export_audio_file(audio_bytes, filename="chant_output.wav"):
    with open(filename, "wb") as f:
        f.write(audio_bytes)
