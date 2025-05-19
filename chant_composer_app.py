
import streamlit as st
st.set_page_config(page_title="Chant Composer", layout="centered")
st.title("🕉️ Chant Composer")
chant = st.text_area("Enter your mantra", "ॐ नमः शिवाय")
if st.button("Generate Bhāva Waveform"):
    st.success(f"Mantra processed: {chant}")
