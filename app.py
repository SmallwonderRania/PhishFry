import streamlit as st
import tensorflow as tf
import pickle
import numpy as np
import base64
import os

# -------------------
# Load Model + Tokenizer
# -------------------
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("phish_model.h5")

@st.cache_resource
def load_tokenizer():
    with open("tokenizer.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()
tokenizer = load_tokenizer()

# -------------------
# Prediction Function
# -------------------
def predict_url(url):
    seq = tokenizer.texts_to_sequences([url])
    padded = tf.keras.preprocessing.sequence.pad_sequences(seq, maxlen=100)
    pred = model.predict(padded)[0][0]
    return pred

# -------------------
# Background + CSS
# -------------------
def add_bg(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                            url("data:image/webp;base64,{encoded}");
                background-size: cover;
                background-position: center;
                color: #f5f5f5;
            }}

            h1, h2, h3, label {{
                color: #ffffff !important;
                text-shadow: 0px 0px 10px rgba(0, 255, 221, 0.8);
            }}

            .stTextInput > div > div > input {{
                background: rgba(0,0,0,0.7);
                color: #00ffdd;
                border: 2px solid #00ffdd;
                border-radius: 12px;
                padding: 10px;
                font-size: 16px;
            }}

            .stButton > button {{
                background: linear-gradient(45deg, #00ffdd, #ff0066);
                color: white;
                border-radius: 12px;
                font-weight: bold;
                padding: 10px 20px;
                transition: 0.3s;
            }}

            .stButton > button:hover {{
                transform: scale(1.05);
                box-shadow: 0px 0px 15px #ff0066;
            }}

            /* ✅ Custom Result Boxes */
            .result {{
                font-size: 22px !important;
                font-weight: bold;
                color: #ffffff !important;   /* Pure white text */
                text-align: center;
                padding: 15px;
                border-radius: 12px;
                margin-top: 15px;
            }}

            .result.success {{
                background: rgba(0, 255, 150, 0.12);
                border: 2px solid #00ffdd;
                text-shadow: 0px 0px 12px #00ffdd;
                box-shadow: 0px 0px 15px rgba(0, 255, 221, 0.8);
            }}

            .result.error {{
                background: rgba(255, 0, 100, 0.12);
                border: 2px solid #ff0066;
                text-shadow: 0px 0px 12px #ff0066;
                box-shadow: 0px 0px 15px rgba(255, 0, 100, 0.8);
            }}

            .result.warning {{
                background: rgba(255, 200, 0, 0.12);
                border: 2px solid #ffcc00;
                text-shadow: 0px 0px 12px #ffcc00;
                box-shadow: 0px 0px 15px rgba(255, 220, 0, 0.9);
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

add_bg("phishingimg.webp")

# -------------------
# UI Layout
# -------------------
st.markdown("<h1>🛡️ PhishFry</h1>", unsafe_allow_html=True)
st.markdown("<h3>CyberGuard – Anti-Phishing System</h3>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Enter a suspicious URL to scan for phishing threats</p>", unsafe_allow_html=True)

url_input = st.text_input("Enter URL", placeholder="https://example.com")

col1, col2, col3 = st.columns([1,1,1])

with col1:
    if st.button("🔍 Scan"):
        if url_input.strip():
            score = predict_url(url_input)
            if score > 0.5:
                st.markdown("<div class='result error'>⚠️ Phishing Detected! Stay Safe.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='result success'>✅ Safe URL</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='result warning'>⚠️ Please enter a URL to scan.</div>", unsafe_allow_html=True)

with col2:
    if st.button("🧹 Clear"):
        st.session_state.url_input = ""
        st.rerun()

with col3:
    if st.button("⬇️ Download Report"):
        st.download_button(
            label="Download Report",
            data=f"URL: {url_input}\nResult: {'Phishing' if score > 0.5 else 'Safe'}",
            file_name="phish_report.txt",
            mime="text/plain"
        )

