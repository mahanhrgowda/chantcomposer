
# bhava_waveform.py

import matplotlib.pyplot as plt
import streamlit as st

def generate_bhava_waveform_chart(vectors):
    if not vectors:
        st.warning("No vectors to display.")
        return
    values = [sum(v) for v in vectors]
    fig, ax = plt.subplots()
    ax.plot(range(len(values)), values, marker='o')
    ax.set_title("Bhāva Intensity Waveform")
    ax.set_xlabel("Syllable Index")
    ax.set_ylabel("Bhāva Intensity")
    st.pyplot(fig)
