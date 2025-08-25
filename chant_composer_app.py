import streamlit as st
import glob
import json
from datetime import timedelta
st.set_page_config(page_title="Sanskrit Chant Composer", layout="wide")
st.title("🕉️ Sanskrit Chant Composer by Bhāva")

# Handle missing custom modules with placeholders
try:
    from bhava_based_mantra_composer import compose_multiple
    from vedic_chant_profile_export_wav import VedicChantProfile
    from bhava_waveform_plotter import export_bhava_waveform
    from animated_bhava_waveform import export_animated_waveform
    from real_time_sanskrit_scanner import scan_text_lines
    from sanskrit_chandas_toolkit.full_bhava_layered_exporter import get_tags_for_syllable
except ModuleNotFoundError as e:
    st.warning(f"Custom module not found: {e}. Using placeholder implementations to allow the app to run.")
    
    def compose_multiple(bhava, count=3, length=5):
        try:
            mantras = []
            for _ in range(count):
                mantra = " ".join([f"syll{i+1}" for i in range(length)])
                mantras.append(mantra)
            return mantras
        except Exception as ex:
            raise RuntimeError(f"Placeholder compose_multiple failed: {ex}")

    class VedicChantProfile:
        def __init__(self, style="default", overlay_meta=True, export_format="mp3"):
            self.style = style
            self.overlay_meta = overlay_meta
            self.export_format = "wav" if export_format == "mp3" else export_format  # Fallback to wav for placeholder

        def chant_and_export(self, chant_data, filename_prefix):
            try:
                import numpy as np
                from scipy.io import wavfile
                import os
                
                # Placeholder: Generate simple sine wave audio for each syllable
                fs = 44100  # Sample rate
                duration = 1.0  # 1 second per syllable
                f = 440.0  # A4 note
                t = np.linspace(0, duration, int(fs * duration), False)
                audio = np.sin(f * t * 2 * np.pi)
                full_audio = np.concatenate([audio for _ in chant_data])
                
                path = f"{filename_prefix}_{self.style}.{self.export_format}"
                wavfile.write(path, fs, full_audio.astype(np.float32))
                
                # Generate placeholder timestamps
                ts_path = f"chant_exports/{filename_prefix}_{self.style}_timestamps.json"
                os.makedirs("chant_exports", exist_ok=True)
                timestamps = []
                current_ms = 0
                ms_per_syllable = int(duration * 1000)
                for idx, data in enumerate(chant_data):
                    timestamps.append({
                        "index": idx,
                        "start_ms": current_ms,
                        "end_ms": current_ms + ms_per_syllable,
                        "syllable": data["syllable"],
                        "bhava": data["bhava"]
                    })
                    current_ms += ms_per_syllable
                with open(ts_path, 'w', encoding='utf-8') as f:
                    json.dump(timestamps, f)
                
                return path
            except Exception as ex:
                raise RuntimeError(f"Placeholder chant_and_export failed: {ex}")

    def export_bhava_waveform(chant_data, filename):
        try:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            x = range(len(chant_data))
            y = [ord(d['bhava'][0]) % 10 + (i % 5) for i, d in enumerate(chant_data)]  # Placeholder waveform data
            ax.plot(x, y)
            ax.set_title("Placeholder Bhāva Waveform")
            plt.savefig(filename)
            plt.close(fig)
        except Exception as ex:
            raise RuntimeError(f"Placeholder export_bhava_waveform failed: {ex}")

    def export_animated_waveform(data, filename):  # Handles both chant_data and timestamps
        try:
            # Placeholder: Create a simple static image as "animation" (no real animation without ffmpeg)
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            if isinstance(data, list) and data and "start_ms" in data[0]:
                x = [t['start_ms'] for t in data]
                y = [t['index'] for t in data]
            else:
                x = range(len(data))
                y = [1] * len(data)
            ax.plot(x, y)
            ax.set_title("Placeholder Animated Waveform (Static)")
            plt.savefig(filename.replace('.mp4', '.png'))  # Save as PNG instead
            with open(filename, 'w') as f:
                f.write("Placeholder video - see static PNG")
            plt.close(fig)
        except Exception as ex:
            raise RuntimeError(f"Placeholder export_animated_waveform failed: {ex}")

    def scan_text_lines(lines):
        try:
            report = []
            for line in lines:
                syllables = [s.strip() + "+phon" for s in line.split() if s.strip()]  # Placeholder syllables with phonemes
                report.append({"syllables": syllables})
            return report
        except Exception as ex:
            raise RuntimeError(f"Placeholder scan_text_lines failed: {ex}")

    def get_tags_for_syllable(phonemes):
        try:
            bh = "placeholder_bhava"
            ck = "placeholder_chandas"
            bt = "placeholder_bt"
            return bh, ck, bt
        except Exception as ex:
            raise RuntimeError(f"Placeholder get_tags_for_syllable failed: {ex}")

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
                phonemes = s.split("+")
                bh, ck, bt = get_tags_for_syllable(phonemes)
                chant_data.append({"syllable": s, "bhava": bh})
        
        base_name = f"chant_{bhava.replace(' ', '_')}"
        
        if export_audio:
            try:
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
                    try:
                        st.video(scwave_path)
                    except Exception as vid_err:
                        st.warning(f"Could not display video: {vid_err}. Check if file exists.")
                else:
                    st.warning("No timestamp file found.")
            except Exception as audio_err:
                st.error(f"Error in audio export section: {audio_err}")
        
        if export_waveform:
            try:
                wpath = f"{base_name}_waveform.png"
                export_bhava_waveform(chant_data, filename=wpath)
                st.image(wpath, caption="Bhāva Waveform")
            except Exception as wave_err:
                st.error(f"Error exporting waveform: {wave_err}")
        
        if export_animation:
            try:
                apath = f"{base_name}_animated.mp4"
                export_animated_waveform(chant_data, filename=apath)
                st.video(apath)
            except Exception as anim_err:
                st.error(f"Error exporting animation: {anim_err}")
    except Exception as main_err:
        st.error(f"Error in mantra composition: {main_err}")
