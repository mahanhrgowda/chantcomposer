
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from scipy.io.wavfile import write as write_wav
import io
import time
import tempfile

st.set_page_config(page_title="Chant Composer", layout="wide")

st.title("🧠 Chant Composer Web App with Bhāva Visuals")
st.markdown("Real-time Bhāva waveform + Chakra visualization from synthesized chants.")

# Synthesizing a sine wave chant (placeholder for real TTS chant)
def synthesize_sine_wave(freq=432, duration=2.0, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    waveform = 0.5 * np.sin(2 * np.pi * freq * t)
    audio = np.int16(waveform * 32767)
    return sample_rate, audio

# Save and return WAV file path
def generate_wav_file():
    sample_rate, audio = synthesize_sine_wave()
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write_wav(temp_wav.name, sample_rate, audio)
    return temp_wav.name

# Plotting Bhāva waveform (mock sinusoidal)
def plot_waveform():
    fig, ax = plt.subplots()
    t = np.linspace(0, 2.0, 44100)
    y = 0.5 * np.sin(2 * np.pi * 432 * t)
    ax.plot(t[:1000], y[:1000])  # Display a small segment for clarity
    ax.set_title("Bhāva Waveform Snapshot")
    st.pyplot(fig)

# Display
plot_waveform()

st.markdown("### 🔉 Audio Playback")
wav_file = generate_wav_file()
audio_bytes = open(wav_file, "rb").read()
st.audio(audio_bytes, format="audio/wav")
