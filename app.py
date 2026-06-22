# deps: pip install streamlit audio-recorder-streamlit faster-whisper soundfile openai==0.28.* edge-tts
import io
import numpy as np
import soundfile as sf
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from faster_whisper import WhisperModel
import openai  # legacy SDK (0.28.*)

# --- DEMO ONLY: 
OPENAI_API_KEY = ""
openai.api_key = OPENAI_API_KEY

st.set_page_config(
    page_title="CareVoice AI",
    page_icon="🩺",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef8f7 0%, #f7fbff 45%, #eef5ff 100%);
}

.block-container {
    padding-top: 2rem;
    max-width: 980px;
}

.hero {
    padding: 2rem;
    border-radius: 26px;
    background: linear-gradient(135deg, #0f766e 0%, #2563eb 100%);
    color: white;
    box-shadow: 0 22px 55px rgba(15, 118, 110, 0.24);
    margin-bottom: 1.5rem;
}

.hero h1 {
    font-size: 2.5rem;
    margin-bottom: 0.35rem;
    font-weight: 800;
}

.hero p {
    font-size: 1.08rem;
    opacity: 0.95;
    margin-bottom: 0;
}

.health-card {
    padding: 1.35rem 1.5rem;
    border-radius: 22px;
    background: rgba(255,255,255,0.86);
    border: 1px solid rgba(37,99,235,0.12);
    box-shadow: 0 12px 32px rgba(15,23,42,0.08);
    margin-bottom: 1rem;
}

.metric-row {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-bottom: 1.25rem;
}

.pill {
    padding: 0.55rem 0.85rem;
    border-radius: 999px;
    background: rgba(15,118,110,0.10);
    color: #0f766e;
    font-weight: 700;
    font-size: 0.9rem;
    border: 1px solid rgba(15,118,110,0.14);
}

h2, h3 {
    color: #0f766e;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #eef8f7 100%);
    border-right: 1px solid rgba(15,118,110,0.12);
}

button {
    border-radius: 999px !important;
}

audio {
    width: 100%;
    border-radius: 14px;
}

.stAlert {
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🩺 CareVoice AI</h1>
    <p>Clinical-style voice assistant powered by Whisper transcription and OpenAI response generation.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="metric-row">
    <div class="pill">🎙️ Click-to-record</div>
    <div class="pill">🧠 Whisper transcription</div>
    <div class="pill">💬 OpenAI legacy SDK</div>
    <div class="pill">🔊 Optional TTS</div>
</div>
""", unsafe_allow_html=True)

# ---- Sidebar settings ----
with st.sidebar:
    st.header("🩺 CareVoice Settings")
    st.caption("Configure the assistant without changing the demo flow.")

    model_name = st.text_input("OpenAI model", value="gpt-3.5-turbo")

    system_prompt = st.text_area(
        "System instructions",
        value="You are a helpful, concise voice assistant. Reply in 1–3 sentences."
    )

    enable_tts = st.toggle("Speak reply (Edge TTS)", value=False)

    voice_name = st.text_input(
        "Edge TTS voice",
        value="en-US-JennyNeural",
        disabled=not enable_tts
    )

    st.markdown("---")
    st.markdown("Run:")
    st.code("python3 -m streamlit run app.py --server.fileWatcherType=poll")

# ---- Load ASR (Whisper via faster-whisper) ----
@st.cache_resource
def load_asr():
    # CPU-friendly; switch to device='cuda' and compute_type='float16' if you have GPU
    return WhisperModel("base", device="cpu", compute_type="int8")

asr = load_asr()

TARGET_SR = 16000

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

def resample_to_16k(int16_data: np.ndarray, sr: int) -> np.ndarray:
    if sr == TARGET_SR:
        return int16_data
    ratio = TARGET_SR / float(sr)
    idx = (np.arange(int(len(int16_data) * ratio)) / ratio).astype(np.int64)
    idx = np.clip(idx, 0, len(int16_data) - 1)
    return int16_data[idx]

def transcribe_wav_bytes(wav_bytes: bytes) -> str:
    data, sr = sf.read(io.BytesIO(wav_bytes), dtype="int16", always_2d=False)
    if data.ndim == 2:
        data = data.mean(axis=1).astype(np.int16)

    data_16k = resample_to_16k(data, sr)

    buf = io.BytesIO()
    sf.write(buf, data_16k, TARGET_SR, subtype="PCM_16", format="WAV")
    buf.seek(0)

    segs, _ = asr.transcribe(buf, language="en")
    return "".join(s.text for s in segs).strip()

def ask_openai_legacy(user_text: str, model: str) -> str:
    # ChatCompletion API (legacy SDK)
    r = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        temperature=0.7,
    )
    return r["choices"][0]["message"]["content"].strip()

async def tts_edge_async(text: str, voice: str) -> bytes:
    import edge_tts  # lazy import so app runs without it
    out = io.BytesIO()
    async for chunk in edge_tts.Communicate(text, voice).stream():
        if chunk["type"] == "audio":
            out.write(chunk["data"])
    return out.getvalue()

# ---- Record audio (no WebRTC) ----
st.markdown('<div class="health-card">', unsafe_allow_html=True)
st.subheader("🎙️ Voice Capture")
st.write("Click the round button to record, then click again to stop.")
audio_bytes = audio_recorder(text="")
st.markdown('</div>', unsafe_allow_html=True)

if audio_bytes:
    st.markdown('<div class="health-card">', unsafe_allow_html=True)
    st.subheader("🔈 Recorded Audio")
    st.audio(audio_bytes, format="audio/wav")
    st.markdown('</div>', unsafe_allow_html=True)

    with st.spinner("Transcribing…"):
        user_text = transcribe_wav_bytes(audio_bytes)

    if user_text:
        st.session_state.transcript += (
            "" if not st.session_state.transcript else " "
        ) + user_text

        st.markdown('<div class="health-card">', unsafe_allow_html=True)
        st.subheader("📝 Patient-style Transcript")
        st.write(st.session_state.transcript)
        st.markdown('</div>', unsafe_allow_html=True)

        with st.spinner("Asking OpenAI…"):
            try:
                answer = ask_openai_legacy(user_text, model_name)
            except Exception as e:
                answer = f"(OpenAI error: {e})"

        st.markdown('<div class="health-card">', unsafe_allow_html=True)
        st.markdown("### 🤖 Assistant Response")
        st.write(answer or "(no reply)")
        st.markdown('</div>', unsafe_allow_html=True)

        if enable_tts and answer and not answer.startswith("(OpenAI error"):
            try:
                import asyncio
                mp3 = asyncio.run(tts_edge_async(answer, voice_name))

                st.markdown('<div class="health-card">', unsafe_allow_html=True)
                st.subheader("🔊 Spoken Reply")
                st.audio(mp3, format="audio/mp3")
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"TTS error: {e}")

else:
    st.markdown('<div class="health-card">', unsafe_allow_html=True)
    st.subheader("📝 Patient-style Transcript")
    st.write(
        st.session_state.transcript
        or "No transcript yet. Record a short message to begin."
    )
    st.markdown('</div>', unsafe_allow_html=True)
