# Streamlit App Entry Point

import streamlit as st

st.title('Chant Composer WebApp')
st.write('Welcome to the Bhāva-Driven Sanskrit Chant Composer!')


import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def generate_bhava_waveform(mantra: str):
    syllables = list(mantra.replace(" ", ""))
    n = len(syllables)
    time = np.linspace(0, 2 * np.pi, n)
    bhava_intensity = np.abs(np.sin(time) * np.random.uniform(0.6, 1.0, n))

    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(time, bhava_intensity, marker='o', linestyle='-', linewidth=2)
    ax.set_xticks(time)
    ax.set_xticklabels(syllables, fontsize=12)
    ax.set_ylabel("Bhāva Intensity")
    ax.set_title("Bhāva Waveform Visualization")
    ax.grid(True)
    st.pyplot(fig)

st.subheader("🔊 Bhāva Waveform Generator")
mantra_input = st.text_input("Enter a Sanskrit Mantra:", "ॐ नमः शिवाय")

if st.button("Generate Bhāva Waveform"):
    generate_bhava_waveform(mantra_input)



import io
import time
from pydub.generators import Sine
from pydub import AudioSegment
import matplotlib.animation as animation
from matplotlib.patches import Circle

def synthesize_audio_from_syllables(syllables):
    base_freq = 220  # Hz
    duration_ms = 400  # per syllable
    audio = AudioSegment.silent(duration=0)

    for i, syllable in enumerate(syllables):
        freq = base_freq + i * 40
        sine_wave = Sine(freq).to_audio_segment(duration=duration_ms).apply_gain(-6)
        audio += sine_wave

    return audio

def generate_chakra_aura(index, total):
    hues = np.linspace(0, 1, total)
    return plt.cm.hsv(hues[index])

def generate_animated_waveform(mantra: str, output_path="bhava_waveform.mp4"):
    syllables = list(mantra.replace(" ", ""))
    n = len(syllables)
    time_vals = np.linspace(0, 2 * np.pi, n)
    bhava_intensity = np.abs(np.sin(time_vals) * np.random.uniform(0.6, 1.0, n))

    fig, ax = plt.subplots(figsize=(8, 4))
    line, = ax.plot([], [], 'o-', lw=2)
    aura = Circle((0, 0), 0.1, color='none')
    ax.add_patch(aura)
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(0, 1.2)
    ax.set_xticks(time_vals)
    ax.set_xticklabels(syllables)
    ax.set_ylabel("Bhāva Intensity")
    ax.set_title("Real-Time Bhāva Waveform with Chakra Auras")

    def init():
        line.set_data([], [])
        aura.set_color('none')
        return line, aura

    def update(frame):
        x = time_vals[:frame + 1]
        y = bhava_intensity[:frame + 1]
        line.set_data(x, y)
        if frame < len(time_vals):
            aura.set_center((time_vals[frame], bhava_intensity[frame]))
            aura.set_radius(0.08 + 0.02 * np.sin(frame))
            aura.set_color(generate_chakra_aura(frame, len(syllables)))
        return line, aura

    ani = animation.FuncAnimation(fig, update, frames=n, init_func=init,
                                  interval=400, blit=True, repeat=False)
    ani.save(output_path, writer='ffmpeg', fps=2)
    plt.close(fig)
    return output_path

st.subheader("🎞️ Real-Time Bhāva Audio + Chakra Animation")
mantra = st.text_input("Enter mantra for synced waveform:", "ॐ नमः शिवाय")
if st.button("🎬 Generate Animated Waveform & Audio"):
    with st.spinner("Synthesizing audio and animation..."):
        syllables = list(mantra.replace(" ", ""))
        audio = synthesize_audio_from_syllables(syllables)
        audio_path = "chant_audio.wav"
        video_path = generate_animated_waveform(mantra)
        audio.export(audio_path, format="wav")
        st.success("🎧 Audio and 🎞️ Video generated!")
        st.audio(audio_path)
        with open(video_path, "rb") as f:
            st.download_button("⬇️ Download Animated MP4", f, file_name="bhava_waveform.mp4", mime="video/mp4")



import hashlib
import qrcode
from PIL import Image
import base64
import json

def generate_maheshwara_hash(mantra: str) -> str:
    # Generate a visual Maheshwara Hash using SHA256 as a symbolic placeholder
    return hashlib.sha256(mantra.encode("utf-8")).hexdigest()

def generate_qr_code_from_data(data: str, path="chant_qr.png") -> str:
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path)
    return path

st.subheader("🕉️ Maheshwara Hash & 📡 Chant QR Verification")

mantra_for_hash = st.text_input("Enter mantra for Maheshwara Hash & QR Code:", "ॐ नमः शिवाय")
if st.button("Generate Hash & QR"):
    hash_str = generate_maheshwara_hash(mantra_for_hash)
    st.code(hash_str, language="text")

    qr_path = generate_qr_code_from_data(hash_str)
    st.image(qr_path, caption="🔗 QR Code of Maheshwara Hash")

    waveform_link = f"https://chantcomposer.streamlit.app/?mantra={base64.urlsafe_b64encode(mantra_for_hash.encode()).decode()}"
    st.markdown(f"[🔗 View with waveform sync]({waveform_link})")



import difflib

st.subheader("🔐 Visual Hash Signature Comparison Tool")

hash_input_1 = st.text_input("Enter Hash 1 (e.g., from mantra A)")
hash_input_2 = st.text_input("Enter Hash 2 (e.g., from mantra B)")

if st.button("Compare Hashes"):
    if hash_input_1 and hash_input_2:
        diff = difflib.ndiff(hash_input_1, hash_input_2)
        diff_visual = ''.join(['🟥' if c.startswith('-') else '🟩' if c.startswith('+') else '⚪' for c in diff])
        st.markdown(f"**Visual Diff:** {diff_visual}")
    else:
        st.warning("Enter both hashes to compare.")



from pyzbar.pyzbar import decode
import cv2

st.subheader("📲 Upload QR Code to Decode Mantra Hash")

uploaded_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    decoded_objs = decode(image)
    if decoded_objs:
        for obj in decoded_objs:
            data = obj.data.decode("utf-8")
            st.success(f"📥 Decoded Data: `{data}`")
    else:
        st.error("❌ No valid QR code detected.")



import sounddevice as sd
import numpy as np
import streamlit as st
from scipy.io.wavfile import write
import tempfile
from ai_classifier.classifier_stub import predict_bhava_from_waveform

st.subheader("🎤 Live Chant Bhāva Prediction")

duration = 5  # seconds
fs = 44100

if st.button("🎙 Record Chant (5s)"):
    st.info("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        write(f.name, fs, recording)
        waveform = recording.flatten()
        predicted = predict_bhava_from_waveform(waveform)
        st.audio(f.name)
        st.success(f"🧠 Predicted Bhāva: **{predicted}**")



import matplotlib.pyplot as plt

def plot_bhava_radar(student_scores, reference_scores):
    labels = list(student_scores.keys())
    student_vals = list(student_scores.values())
    reference_vals = list(reference_scores.values())

    student_vals += student_vals[:1]
    reference_vals += reference_vals[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax.plot(angles, student_vals, label="Student", color="orange")
    ax.fill(angles, student_vals, alpha=0.3)
    ax.plot(angles, reference_vals, label="Guru", color="green")
    ax.fill(angles, reference_vals, alpha=0.2)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_title("🔬 Bhāva Profile Match")
    ax.legend()
    st.pyplot(fig)

st.subheader("📊 Bhāva Grading Radar Chart")

example_student = {
    "Śāntiḥ": 0.7, "Bhaktiḥ": 0.6, "Premaḥ": 0.5, "Vīraḥ": 0.8,
    "Karunā": 0.4, "Raudraḥ": 0.2, "Adbhutam": 0.5, "Hāsyaḥ": 0.6,
    "Bhayānakaḥ": 0.3, "Bībhatsaḥ": 0.2
}
example_guru = {
    "Śāntiḥ": 0.9, "Bhaktiḥ": 0.8, "Premaḥ": 0.7, "Vīraḥ": 0.9,
    "Karunā": 0.6, "Raudraḥ": 0.4, "Adbhutam": 0.6, "Hāsyaḥ": 0.7,
    "Bhayānakaḥ": 0.4, "Bībhatsaḥ": 0.3
}

if st.button("Generate Example Grading Chart"):
    plot_bhava_radar(example_student, example_guru)
