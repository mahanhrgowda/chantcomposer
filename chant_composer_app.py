import streamlit as st
import random
import re
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import os
import json
from datetime import timedelta
import glob

st.set_page_config(page_title="Sanskrit Chant Composer", layout="wide")
st.title("🕉️ Sanskrit Chant Composer by Bhāva")

# Define bhava-specific word lists based on research
bhava_words = {
    "Śāntiḥ (peace)": ['om', 'shanti', 'dyauha', 'antariksha', 'prithivi', 'apah', 'oshadhayah', 'vanaspatayah', 'vishvedevah', 'brahma', 'sarvam', 'shantireva'],
    "Prema (love)": ['aham', 'prema', 'hare', 'krishna', 'hare', 'rama'],
    "Vīrya (valor)": ['om', 'veera', 'virya', 'vijay', 'bal', 'hanuman', 'namah'],
    "Bhaya (fear)": ['om', 'dum', 'durgayei', 'namaha', 'shante', 'prashante', 'sarva', 'bhaya', 'upasha', 'mani', 'swaha'],
    "Āścarya (wonder)": ['om', 'bhur', 'bhuvah', 'svah', 'tat', 'savitur', 'varenyam', 'bhargo', 'devasya', 'dhimahi', 'dhiyo', 'yo', 'nah', 'prachodayat'],
    "Karunā (compassion)": ['om', 'mani', 'padme', 'hum', 'karuna', 'namah'],
    "Harṣa (joy)": ['hare', 'krishna', 'hare', 'rama', 'govinda', 'gopala'],
    "Titikṣā (forbearance)": ['om', 'titiksha', 'namah', 'durga', 'namah', 'shiva', 'namah'],
    "Dhairya (patience)": ['om', 'dhairya', 'namah', 'jat', 'pahāra', 'dhīraj', 'shanti']
}

# Function to count syllables (approximate based on vowels)
def count_syllables(word):
    vowels = 'aeiouāīūṛṝḷḹ'
    return sum(1 for c in word.lower() if c in vowels)

# Compose multiple mantras
def compose_multiple(bhava, count=3, length=5):
    words = bhava_words.get(bhava, ['om', 'namah', 'shivaya'])  # Fallback
    mantras = []
    for _ in range(count):
        mantra_words = []
        current_syl = 0
        while current_syl < length:
            w = random.choice(words)
            syl = count_syllables(w)
            if current_syl + syl <= length:
                mantra_words.append(w)
                current_syl += syl
            else:
                # Add a short syllable if needed
                if length - current_syl == 1:
                    mantra_words.append('om')
                break
        mantras.append(' '.join(mantra_words))
    return mantras

# Scan text lines for syllables
def scan_text_lines(lines):
    report = []
    for line in lines:
        syllables = []
        for word in line.split():
            # Simple syllable splitter for Romanized Sanskrit
            syls = re.findall(r'[bcdfghjklmnpqrstvwxyzḥśṣñṅṇṁṃ]*[aeiouāīūṛṝḷḹ][bcdfghjklmnpqrstvwxyzḥśṣñṅṇṁṃ]*', word, re.IGNORECASE)
            syllables.extend(syls)
        report.append({"syllables": syllables})
    return report

# Get tags for syllable: bhava, chandas (laghu/guru), bt (tone placeholder)
def get_tags_for_syllable(phonemes):
    syllable = ''.join(phonemes)  # Since phonemes might be split, but here simple
    # Determine chandas: guru if long vowel or complex
    long_vowels = 'āīūṛḹeiaoau'
    if any(v in syllable.lower() for v in long_vowels) or len(re.findall(r'[bcdfghjklmnpqrstvwxyzḥśṣñṅṇṁṃ]{2,}', syllable)) > 0:
        ck = 'guru'
    else:
        ck = 'laghu'
    bh = 'bhava_tag'  # Placeholder, can be dynamic
    bt = 'default_bt'
    return bh, ck, bt

# Vedic Chant Profile class
class VedicChantProfile:
    def __init__(self, style="default", overlay_meta=True, export_format="wav"):
        self.style = style
        self.overlay_meta = overlay_meta
        self.export_format = export_format

    def chant_and_export(self, chant_data, filename_prefix):
        fs = 44100  # Sample rate
        duration = 0.5  # Duration per syllable in seconds
        low_freq, med_freq, high_freq = 220, 440, 660

        full_audio = np.array([])
        timestamps = []
        current_ms = 0
        ms_per_syl = int(duration * 1000)

        for idx, data in enumerate(chant_data):
            t = np.linspace(0, duration, int(fs * duration), False)
            
            if self.style == "udatta":
                freq = high_freq
                tone = np.sin(freq * t * 2 * np.pi)
            elif self.style == "svarita":
                # Glide high to low
                freqs = np.linspace(high_freq, low_freq, len(t))
                tone = np.sin(2 * np.pi * np.cumsum(freqs / fs))
            elif self.style == "zigzag":
                freq = high_freq if idx % 2 == 0 else low_freq
                tone = np.sin(freq * t * 2 * np.pi)
            else:  # default
                freq = med_freq
                tone = np.sin(freq * t * 2 * np.pi)
            
            # Normalize
            tone = tone * 0.5 / np.max(np.abs(tone))
            full_audio = np.append(full_audio, tone)
            
            timestamps.append({
                "index": idx,
                "start_ms": current_ms,
                "end_ms": current_ms + ms_per_syl,
                "syllable": data["syllable"],
                "bhava": data["bhava"]
            })
            current_ms += ms_per_syl
        
        path = f"{filename_prefix}_{self.style}.{self.export_format}"
        wavfile.write(path, fs, full_audio.astype(np.float32))
        
        # Save timestamps
        os.makedirs("chant_exports", exist_ok=True)
        ts_path = f"chant_exports/{filename_prefix}_{self.style}_timestamps.json"
        with open(ts_path, 'w', encoding='utf-8') as f:
            json.dump(timestamps, f)
        
        return path

# Export bhava waveform
def export_bhava_waveform(chant_data, filename):
    x = range(len(chant_data))
    # Map bhava to a value for y
    bhava_map = {bh: i for i, bh in enumerate(bhava_words.keys())}
    y = [bhava_map.get(d['bhava'], 0) + random.uniform(-0.5, 0.5) for d in chant_data]
    fig, ax = plt.subplots()
    ax.plot(x, y, color='blue')
    ax.set_title("Bhāva Waveform")
    ax.set_xlabel("Syllable Index")
    ax.set_ylabel("Bhāva Intensity")
    plt.savefig(filename)
    plt.close(fig)

# Export animated waveform (static placeholder due to limitations)
def export_animated_waveform(data, filename):
    # For now, create a static plot as placeholder
    fig, ax = plt.subplots()
    if isinstance(data, list) and data and "start_ms" in data[0]:
        x = [t['start_ms'] / 1000 for t in data]
        y = [t['index'] + random.uniform(-1, 1) for t in data]
    else:
        x = range(len(data))
        y = [ord(d['bhava'][0]) % 10 for d in data]
    ax.plot(x, y, color='green')
    ax.set_title("Animated Waveform (Static Placeholder)")
    static_filename = filename.replace('.mp4', '.png')
    plt.savefig(static_filename)
    plt.close(fig)
    # Write placeholder for video
    with open(filename, 'w') as f:
        f.write("Placeholder video file - see static PNG for waveform.")

# Sidebar
st.sidebar.header("🎛️ Chant Settings")
bhava = st.sidebar.selectbox("Choose Bhāva (Emotion)", list(bhava_words.keys()))
count = st.sidebar.slider("Number of Mantras", 1, 10, 3)
length = st.sidebar.slider("Syllables per Mantra", 3, 10, 5)
chant_style = st.sidebar.selectbox("Chant Style", ["default", "udatta", "svarita", "zigzag"])
export_audio = st.sidebar.checkbox("Export Audio (WAV)", value=True)
export_waveform = st.sidebar.checkbox("Export Bhāva Waveform Chart")
export_animation = st.sidebar.checkbox("Export Animated Bhāva Video")

# Main logic
if st.button("🪔 Compose Mantras"):
    try:
        mantras = compose_multiple(bhava, count=count, length=length)
        st.subheader(f"🧘‍♂️ Composed Mantras for: {bhava}")
        for i, m in enumerate(mantras):
            st.markdown(f"**{i+1}.** _{m}_")
        
        chant_line = " ".join(mantras)
        report = scan_text_lines([chant_line])
        
        chant_data = []
        for line in report:
            for s in line["syllables"]:
                phonemes = [s]  # Simple, no + split
                bh_tag, ck, bt = get_tags_for_syllable(phonemes)
                chant_data.append({"syllable": s, "bhava": bhava})  # Use selected bhava
        
        base_name = f"chant_{bhava.replace(' ', '_').replace('(', '').replace(')', '')}"
        
        if export_audio:
            profile = VedicChantProfile(style=chant_style, overlay_meta=True, export_format="wav")
            path = profile.chant_and_export(chant_data, filename_prefix=base_name)
            st.success("Chant audio saved")
            st.audio(path)
            
            # Load timestamps
            ts_path = f"chant_exports/{base_name}_{chant_style}_*timestamps.json"
            matched = glob.glob(ts_path)
            if matched:
                with open(matched[0], "r", encoding="utf-8") as f:
                    timestamps = json.load(f)
                st.subheader("🕒 Timestamp Metadata")
                st.json(timestamps)
                
                # Generate WebVTT
                def ms_to_vtt(ms):
                    td = timedelta(milliseconds=ms)
                    return str(td)[:-3].replace('.', ',')
                
                vtt_lines = ["WEBVTT\n"]
                for t in timestamps:
                    start = ms_to_vtt(t["start_ms"])
                    end = ms_to_vtt(t["end_ms"])
                    text = f"{t['syllable']} ({t['bhava']})"
                    vtt_lines.append(f"{t['index'] + 1}")
                    vtt_lines.append(f"{start} --> {end}")
                    vtt_lines.append(text)
                    vtt_lines.append("")
                
                vtt_path = f"{base_name}_sync.vtt"
                with open(vtt_path, "w", encoding="utf-8") as vf:
                    vf.write("\n".join(vtt_lines))
                st.download_button("⬇️ Download Subtitle (VTT)", data=open(vtt_path, "rb"), file_name=vtt_path)
                
                # Export scrolling animation
                scwave_path = f"{base_name}_scroll.mp4"
                export_animated_waveform(timestamps, filename=scwave_path)
                st.image(scwave_path.replace('.mp4', '.png'), caption="Scrolling Waveform (Static)")
        
        if export_waveform:
            wpath = f"{base_name}_waveform.png"
            export_bhava_waveform(chant_data, filename=wpath)
            st.image(wpath, caption="Bhāva Waveform")
        
        if export_animation:
            apath = f"{base_name}_animated.mp4"
            export_animated_waveform(chant_data, filename=apath)
            st.image(apath.replace('.mp4', '.png'), caption="Animated Waveform (Static)")
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
