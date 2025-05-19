# chant_composer_app.py

import streamlit as st
import numpy as np
import base64
import json
from phoneme_bhava_mapping import get_bhava_vector, bhava_tags_from_phonemes
from bhava_waveform import generate_bhava_waveform_chart
from chant_profiles import load_chant_profiles
from mantra_audio import synthesize_audio, export_audio_file
from qr_exporter import generate_qr_code, decode_qr_code
from encryption_engine import encrypt_bhava_vectors, decrypt_bhava_vectors

# Chakra animation embed (custom landing)
st.markdown("""
    <div style='text-align:center;'>
        <iframe src="https://chakra-visualizer.streamlit.app" width="100%" height="300" frameborder="0"></iframe>
        <h2>🕉️ Chakra-Activated Chant Composer</h2>
        <p>Explore your sound vibrations as divine frequency maps</p>
    </div>
    <hr>
""", unsafe_allow_html=True)

# App Title and Intro
st.set_page_config(page_title="Chant Composer WebApp", layout="wide")
st.title("🎵 Chant Composer: Bhāva + Phoneme Visualizer")

# Sidebar Setup
with st.sidebar:
    st.header("🧰 Chant Options")
    chant_text = st.text_area("🔤 Enter your mantra or chant", "ॐ नमः शिवाय")
    profile = st.selectbox("🎚️ Select Chant Profile", load_chant_profiles())
    show_waveform = st.checkbox("📈 Show Bhāva Waveform", True)
    show_chakra_overlay = st.checkbox("🌀 Chakra Overlay Mode", True)
    show_aura_visual = st.checkbox("🌈 Aura Visualization", False)
    export_qr = st.checkbox("📦 Export as QR Code", True)
    synthesize = st.button("🔊 Synthesize Chant Audio")
    encrypt = st.button("🔐 Encrypt and Export")

# Phoneme + Bhāva Processing
st.subheader("🔡 Phoneme & Bhāva Mapping")
phoneme_vectors = get_bhava_vector(chant_text)
bhava_tags = bhava_tags_from_phonemes(phoneme_vectors)
st.write("Bhāva Tags:", bhava_tags)

# Bhāva Waveform Chart
if show_waveform:
    st.subheader("📈 Bhāva Intensity Waveform")
    generate_bhava_waveform_chart(phoneme_vectors)

# Audio Synthesis
if synthesize:
    st.subheader("🔊 Audio Output")
    audio_bytes = synthesize_audio(chant_text)
    st.audio(audio_bytes, format='audio/wav')
    export_audio_file(audio_bytes, filename="chant_output.wav")

# Encryption + QR Export
if encrypt:
    st.subheader("🔐 Encrypted QR Output")
    encrypted = encrypt_bhava_vectors(phoneme_vectors)
    b64_data = base64.b64encode(json.dumps(encrypted).encode()).decode()
    st.code(b64_data, language='text')
    qr_img = generate_qr_code(b64_data)
    st.image(qr_img, caption="Scan to Decode Bhāva Vector")

# Optional QR Decoder
with st.expander("📥 QR Code Decoder"):
    uploaded_qr = st.file_uploader("Upload QR Image", type=["png", "jpg"])
    if uploaded_qr:
        decoded = decode_qr_code(uploaded_qr)
        de_b64 = base64.b64decode(decoded).decode()
        decrypted = decrypt_bhava_vectors(json.loads(de_b64))
        st.json(decrypted)

# Chakra Overlay and Aura Visual
if show_chakra_overlay:
    st.subheader("🌀 Chakra Visualization")
    st.markdown("Chakra glow synced to chant progression.")
    # (Insert Chakra animation integration here)

if show_aura_visual:
    st.subheader("🌈 Aura Field Rendering")
    st.markdown("Dynamic aura field mapped from Bhāva frequency.")
    # (Insert aura visualization rendering logic here)

st.markdown("---")
st.markdown("Crafted with ❤️ for vibrational coding and spiritual resonance ✨")
