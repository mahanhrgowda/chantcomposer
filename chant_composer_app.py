
import streamlit as st
from bhava_based_mantra_composer import compose_multiple
from vedic_chant_profile_export_wav import VedicChantProfile
from bhava_waveform_plotter import export_bhava_waveform
from animated_bhava_waveform import export_animated_waveform
from real_time_sanskrit_scanner import scan_text_lines
from sanskrit_chandas_toolkit.full_bhava_layered_exporter import get_tags_for_syllable

import glob
import json
from datetime import timedelta

st.set_page_config(page_title="Sanskrit Chant Composer", layout="wide")
st.title("🕉️ Sanskrit Chant Composer by Bhāva")

# Sidebar configuration
st.sidebar.header("🎛️ Chant Settings")
bhava = st.sidebar.selectbox("Choose Bhāva (Emotion)", [
    "Śāntiḥ (peace)", "Prema (love)", "Vīrya (valor)", "Bhaya (fear)",
    "Āścarya (wonder)", "Karunā (compassion)", "Harṣa (joy)",
    "Titikṣā (forbearance)", "Dhairya (patience)"
])
count = st.sidebar.slider("Number of Mantras", 1, 10, 3)
length = st.sidebar.slider("Syllables per Mantra", 3, 10, 5)
chant_style = st.sidebar.selectbox("Chant Style", ["default", "udatta", "svarita", "zigzag"])
export_audio = st.sidebar.checkbox("Export MP3 Audio", value=True)
export_waveform = st.sidebar.checkbox("Export Bhāva Waveform Chart")
export_animation = st.sidebar.checkbox("Export Animated Bhāva Video")

# Compose mantras
if st.button("🪔 Compose Mantras"):
    mantras = compose_multiple(bhava, count=count, length=length)
    st.subheader(f"🧘‍♂️ Composed Mantras for: {bhava}")
    for i, m in enumerate(mantras):
        st.markdown(f"**{i+1}.** _{m}_")

    chant_line = " ".join(mantras)
    report = scan_text_lines([chant_line])
    chant_data = []
    for line in report:
        for s in line["syllables"]:
            phonemes = s.split("+")
            bh, ck, bt = get_tags_for_syllable(phonemes)
            chant_data.append({"syllable": s, "bhava": bh})

    base_name = f"chant_{bhava.replace(' ', '_')}"

    if export_audio:
        profile = VedicChantProfile(style=chant_style, overlay_meta=True, export_format="mp3")
        path = profile.chant_and_export(chant_data, filename_prefix=base_name)
        st.success("Chant audio saved")
        st.audio(path)

        # Load timestamps and show metadata
        ts_path = f"chant_exports/{base_name}_{chant_style}_*.json"
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
            st.video(scwave_path)

    if export_waveform:
        wpath = f"{base_name}_waveform.png"
        export_bhava_waveform(chant_data, filename=wpath)
        st.image(wpath, caption="Bhāva Waveform")

    if export_animation:
        apath = f"{base_name}_animated.mp4"
        export_animated_waveform(chant_data, filename=apath)
        st.video(apath)
