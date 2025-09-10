import streamlit as st
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="EchoVerse", layout="wide")

st.title("🎧 EchoVerse - AI Audiobook Generator")

# Text Input Section
uploaded_file = st.file_uploader("📄 Upload .txt File", type="txt")
text_input = st.text_area("Or paste your text here", height=200)

if uploaded_file is not None:
    text_input = uploaded_file.getvalue().decode("utf-8")

tone = st.selectbox("🎭 Choose a Tone", ["Neutral", "Suspenseful", "Inspiring"])
voice = st.selectbox("🗣️ Choose Voice", ["Allison", "Michael", "Lisa"])

# Placeholder for LLM response
def rewrite_text(text, tone):
    # Mock LLM rewrite
    return f"[{tone} Version]: {text}"

# IBM Watson TTS
def synthesize_speech(text, voice):
    authenticator = IAMAuthenticator(os.getenv("IBM_API_KEY"))
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(os.getenv("IBM_URL"))

    response = tts.synthesize(
        text,
        voice=f'en-US_{voice}V3Voice',
        accept='audio/mp3'
    ).get_result()

    return response.content

if st.button("✨ Generate Audiobook"):
    if not text_input:
        st.error("Please provide input text.")
    else:
        rewritten = rewrite_text(text_input, tone)

        st.subheader("📘 Original vs Rewritten")
        col1, col2 = st.columns(2)
        with col1:
            st.text_area("Original Text", text_input, height=250)
        with col2:
            st.text_area("Rewritten Text", rewritten, height=250)

        with st.spinner("🎙️ Generating Audio..."):
            audio = synthesize_speech(rewritten, voice)
            st.audio(audio, format="audio/mp3")
            st.download_button("⬇️ Download MP3", audio, file_name="echoverse.mp3")
