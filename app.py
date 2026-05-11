from __future__ import annotations

import base64
import html
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from pipeline import run_assistant
from translator import LANGUAGE_OPTIONS


UPLOAD_DIR = Path("uploads/crop_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
LOGO_PATH = Path(__file__).parent / "assets" / "agro-doc-logo.png"
LOGO_DATA_URI = ""
if LOGO_PATH.exists():
    LOGO_DATA_URI = "data:image/png;base64," + base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")


st.set_page_config(
    page_title="AGRO-DOC Smart Assistant",
    page_icon=":seedling:",
    layout="wide",
)

for key, value in {
    "question": "",
    "signed_in": False,
    "user_name": "",
    "show_guide": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = value


st.markdown(
    """
<style>
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu,
footer {
    display: none !important;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

.stApp {
    background: #f8fafc;
}

.navbar {
    height: 104px;
    background: #ffffff;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 5rem;
    border-bottom: 1px solid #e5e7eb;
    box-shadow: 0 4px 20px rgba(15,23,42,0.06);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
}

.logo {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.logo-image {
    height: 88px;
    width: auto;
    max-width: 520px;
    object-fit: contain;
    border-radius: 10px;
}

.logo-title {
    font-size: 1.5rem;
    font-weight: 950;
    color: #111827;
    line-height: 1;
}

.logo-sub {
    color: #138a3d;
    font-size: 0.8rem;
    font-weight: 800;
}

.hero {
    min-height: 430px;
    margin-top: 104px;
    background:
        linear-gradient(110deg, rgba(7,95,37,0.88), rgba(14,90,54,0.78), rgba(28,70,124,0.78)),
        url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1800&q=80");
    background-size: cover;
    background-position: center;
    color: white;
    position: relative;
    overflow: hidden;
    padding: 4rem 5rem 4rem;
}

.hero::before {
    content: "";
    position: absolute;
    width: 95px;
    height: 95px;
    border-radius: 50%;
    background: rgba(255,255,255,0.1);
    left: 3rem;
    top: 5rem;
}

.hero::after {
    content: "";
    position: absolute;
    width: 115px;
    height: 115px;
    border-radius: 50%;
    background: rgba(110,150,255,0.18);
    right: 4rem;
    top: 9rem;
}

.hero-content {
    position: relative;
    z-index: 2;
    text-align: center;
    max-width: 960px;
    margin: 0 auto;
}

.hero h1 {
    font-size: clamp(2.8rem, 5vw, 4.8rem);
    line-height: 1.08;
    font-weight: 950;
    margin: 0;
    color: #ffffff;
}

.hero h2 {
    color: #facc15;
    font-size: clamp(1.5rem, 3vw, 2.3rem);
    font-weight: 950;
    margin: 1rem 0 1.3rem;
}

.hero p {
    color: #f9fafb;
    font-size: 1.08rem;
    line-height: 1.75;
    max-width: 780px;
    margin: 0 auto;
    font-weight: 650;
}

.app-panel {
    max-width: 1180px;
    margin: 2rem auto 0;
    position: relative;
    z-index: 10;
    padding: 0 1rem 3rem;
}

.section-spacer {
    max-width: 1180px;
    margin: 2rem auto 0;
}

div[data-testid="stHorizontalBlock"],
div[data-testid="stTextArea"],
div[data-testid="stFileUploader"],
hr {
    max-width: 1180px;
    margin-left: auto !important;
    margin-right: auto !important;
}

.question-shell {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 24px;
    box-shadow: 0 25px 70px rgba(15,23,42,0.18);
    padding: 1.5rem;
    margin-bottom: 1.7rem;
}

textarea {
    background: #ffffff !important;
    border-radius: 16px !important;
    border: 1.5px solid #d1d5db !important;
    color: #111827 !important;
    caret-color: #0b7a28 !important;
    min-height: 105px !important;
    font-size: 1rem !important;
    line-height: 1.55 !important;
    padding: 1rem !important;
    box-shadow: inset 0 1px 2px rgba(15,23,42,0.05);
}

textarea::placeholder {
    color: #475467 !important;
    opacity: 1 !important;
}

textarea:focus {
    border: 2px solid #16a34a !important;
    outline: none !important;
    box-shadow: 0 0 0 4px rgba(22,163,74,0.18), inset 0 1px 2px rgba(15,23,42,0.05) !important;
}

textarea::selection {
    background: rgba(22,163,74,0.22) !important;
    color: #111827 !important;
}

div[data-testid="stTextArea"] small,
div[data-testid="stTextArea"] [data-testid="InputInstructions"],
div[data-testid="stTextArea"] [data-baseweb="typo-labelsmall"] {
    display: none !important;
}

div.stButton > button {
    border-radius: 14px !important;
    min-height: 3rem !important;
    font-weight: 850 !important;
    background: linear-gradient(135deg, #16c76f, #06964f) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 10px 24px rgba(6,150,79,0.28);
    transition: all 0.25s ease !important;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 35px rgba(6,150,79,0.35);
    background: linear-gradient(135deg, #20d982, #047c42) !important;
    color: white !important;
}

div.stButton > button:disabled {
    background: #e5e7eb !important;
    color: #6b7280 !important;
    box-shadow: none !important;
}

div[data-testid="stSelectbox"] {
    background: linear-gradient(135deg, #16c76f, #06964f);
    border-radius: 14px;
    box-shadow: 0 10px 24px rgba(6,150,79,0.28);
}

div[data-testid="stSelectbox"] > div {
    background: linear-gradient(135deg, #16c76f, #06964f) !important;
    border: none !important;
    border-radius: 14px !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: linear-gradient(135deg, #16c76f, #06964f) !important;
    border: none !important;
    color: #ffffff !important;
    min-height: 3rem !important;
}

div[data-testid="stSelectbox"] span,
div[data-testid="stSelectbox"] svg {
    color: #ffffff !important;
    fill: #ffffff !important;
}

button[title="Mic"],
button[title="Stop"],
button[aria-label="Mic"],
button[aria-label="Stop"] {
    border-radius: 14px !important;
    min-height: 3rem !important;
    font-weight: 850 !important;
    background: linear-gradient(135deg, #16c76f, #06964f) !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 10px 24px rgba(6,150,79,0.28) !important;
}

.mic-shell {
    border-radius: 14px;
    background: linear-gradient(135deg, #16c76f, #06964f);
    box-shadow: 0 10px 24px rgba(6,150,79,0.28);
    overflow: hidden;
}

.guide-box {
    margin: 1.3rem 0;
    border: 1px solid #d9ead8;
    border-radius: 20px;
    background: #f7fff6;
    padding: 1.25rem;
    box-shadow: 0 16px 35px rgba(15,23,42,0.07);
}

.guide-box h3 {
    margin-top: 0;
    color: #0f7a24;
}

.guide-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}

.guide-item {
    background: #ffffff;
    border: 1px solid #e2ecdf;
    border-radius: 16px;
    padding: 1rem;
    color: #111827;
    box-shadow: 0 8px 20px rgba(15,23,42,0.04);
}

.guide-item strong {
    color: #0f7a24;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.2rem;
    margin: 0 auto;
}

.glass-card {
    min-height: 185px;
    border-radius: 22px;
    padding: 1.8rem;
    text-align: center;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    box-shadow: 0 20px 50px rgba(15,23,42,0.08);
    transition: all 0.25s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 28px 65px rgba(15,23,42,0.13);
}

.glass-icon {
    width: 66px;
    height: 66px;
    border-radius: 18px;
    margin: 0 auto 1rem;
    display: grid;
    place-items: center;
    color: white;
    font-size: 1.15rem;
    font-weight: 950;
    background: linear-gradient(135deg, #34d399, #10b981);
    box-shadow: 0 12px 25px rgba(16,185,129,0.3);
}

.glass-card h3 {
    color: #111827;
    margin: 0 0 0.7rem;
    font-size: 1.08rem;
    font-weight: 950;
}

.glass-card p {
    color: #344054;
    margin: 0;
    font-size: 0.92rem;
    line-height: 1.6;
}

.answer-box {
    max-width: 1180px;
    margin: 1.5rem auto 0;
    background: #ffffff;
    color: #111827;
    border-radius: 18px;
    padding: 1.3rem;
    border-left: 6px solid #16a34a;
    box-shadow: 0 16px 35px rgba(15,23,42,0.1);
}

.answer-box h3 {
    color: #087d2a;
    margin-top: 0;
}

.answer-content {
    white-space: pre-wrap;
    line-height: 1.7;
    font-weight: 500;
}

div[data-testid="stFileUploader"] {
    margin-top: 1.2rem;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 1rem;
    box-shadow: 0 14px 35px rgba(15,23,42,0.06);
}

.small-note {
    color: #64748b;
    font-size: 0.9rem;
    max-width: 1180px;
    margin: 0.75rem auto 0.35rem;
    padding: 0 0.25rem;
}

@media (max-width: 900px) {
    .navbar {
        padding: 0 1rem;
        height: 86px;
    }

    .logo-image {
        height: 72px;
        max-width: 320px;
    }

    .hero {
        margin-top: 86px;
        min-height: 470px;
        padding: 3rem 1rem 7rem;
    }

    .app-panel {
        margin-top: -80px;
    }

    .feature-grid,
    .guide-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


logo_markup = (
    f'<img class="logo-image" src="{LOGO_DATA_URI}" alt="AGRO-DOC AI logo">'
    if LOGO_DATA_URI
    else """
        <div>
            <div class="logo-title">AGRO-DOC AI</div>
            <div class="logo-sub">Smart Agriculture Assistant</div>
        </div>
    """
)

st.markdown(
    f"""
<div class="navbar">
    <div class="logo">
        {logo_markup}
    </div>
</div>

<section class="hero">
    <div class="hero-content">
        <h1>Your Smart Farming Companion</h1>
        <h2>Anytime, Anywhere</h2>
        <p>
            Empowering farmers with AI-driven crop advisory, multilingual support,
            crop disease guidance, fertilizer suggestions, and sustainable farming practices.
        </p>
    </div>
</section>
""",
    unsafe_allow_html=True,
)


st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

hero_btn_col1, hero_btn_col2 = st.columns(2)

with hero_btn_col1:
    st.button("Get AI Farming Advice", type="primary", use_container_width=True)

with hero_btn_col2:
    if st.button("Explore Farming Guide", use_container_width=True):
        st.session_state.show_guide = not st.session_state.show_guide

st.markdown("<br>", unsafe_allow_html=True)

lang_col, mic_col, spacer_col = st.columns([1.8, 1.2, 2.0])

with lang_col:
    answer_language_label = st.selectbox(
        "Answer language",
        options=list(LANGUAGE_OPTIONS.keys()),
        index=0,
        label_visibility="collapsed",
    )

with mic_col:
    components.html(
        """
        <button id="agroMicButton" type="button">Mic</button>
        <script>
        const button = document.getElementById("agroMicButton");
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        function setNativeValue(element, value) {
            const valueSetter = Object.getOwnPropertyDescriptor(element, "value")?.set;
            const prototype = Object.getPrototypeOf(element);
            const prototypeValueSetter = Object.getOwnPropertyDescriptor(prototype, "value")?.set;
            if (prototypeValueSetter && valueSetter !== prototypeValueSetter) {
                prototypeValueSetter.call(element, value);
            } else if (valueSetter) {
                valueSetter.call(element, value);
            } else {
                element.value = value;
            }
            element.dispatchEvent(new Event("input", { bubbles: true }));
            element.dispatchEvent(new Event("change", { bubbles: true }));
        }

        button.onclick = () => {
            if (!SpeechRecognition) {
                alert("Voice input is supported in Chrome or Edge.");
                return;
            }

            const doc = window.parent.document;
            const textarea = doc.querySelector("textarea");
            if (!textarea) {
                alert("Question box not found.");
                return;
            }

            const recognition = new SpeechRecognition();
            recognition.lang = "en-IN";
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            button.textContent = "Listening...";
            recognition.onresult = (event) => {
                const spokenText = event.results[0][0].transcript;
                const currentText = textarea.value.trim();
                setNativeValue(textarea, currentText ? `${currentText} ${spokenText}` : spokenText);
                button.textContent = "Mic";
            };
            recognition.onerror = () => {
                button.textContent = "Mic";
            };
            recognition.onend = () => {
                button.textContent = "Mic";
            };
            recognition.start();
        };
        </script>
        <style>
        html, body {
            margin: 0;
            padding: 0;
            background: transparent;
            overflow: hidden;
        }
        #agroMicButton {
            width: 100%;
            min-height: 48px;
            border-radius: 14px;
            border: 0;
            color: #ffffff;
            font: 850 16px Arial, sans-serif;
            background: linear-gradient(135deg, #16c76f, #06964f);
            box-shadow: 0 10px 24px rgba(6,150,79,0.28);
            cursor: pointer;
        }
        #agroMicButton:hover {
            background: linear-gradient(135deg, #20d982, #047c42);
        }
        </style>
        """,
        height=56,
    )

st.markdown(
    '<div class="small-note">Ask about crop disease, fertilizer, irrigation, weather, soil health, or farming schemes.</div>',
    unsafe_allow_html=True,
)

question = st.text_area(
    "Question",
    placeholder="Ask crop, disease, fertilizer, weather, or farming question here...",
    key="question",
    label_visibility="collapsed",
)

ask_left, ask_right = st.columns([5, 1])

with ask_right:
    ask_clicked = st.button("Ask", type="primary", use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)


if st.session_state.show_guide:
    st.markdown(
        """
<div class="guide-box">
    <h3>Practical Farming Guide</h3>
    <div class="guide-grid">
        <div class="guide-item">
            <strong>Crop problem</strong><br>
            Tell crop name, crop age, symptoms, and affected plant part.
        </div>
        <div class="guide-item">
            <strong>Soil and fertilizer</strong><br>
            Share soil type, fertilizer use, irrigation, and crop stage.
        </div>
        <div class="guide-item">
            <strong>Better answer</strong><br>
            Add location, weather, and uploaded image details when possible.
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

feature_cards = [
    ("AI", "Real-time AI Support", "Get instant answers to farming questions using advanced LLM technology."),
    ("ML", "Multilingual Assistant", "Ask questions in your preferred language and get simple farmer-friendly answers."),
    ("CD", "Crop Doctor", "Upload crop images and include symptoms in your question for better guidance."),
]

feature_cols = st.columns(3)
for column, (icon, title, text) in zip(feature_cols, feature_cards):
    with column:
        st.markdown(
            f"""
<div class="glass-card">
    <div class="glass-icon">{icon}</div>
    <h3>{title}</h3>
    <p>{text}</p>
</div>
""",
            unsafe_allow_html=True,
        )


uploaded_file = st.file_uploader(
    "Upload crop image optional",
    type=["jpg", "jpeg", "png"],
)

if uploaded_file:
    image_path = UPLOAD_DIR / uploaded_file.name
    image_path.write_bytes(uploaded_file.getbuffer())
    st.image(str(image_path), caption="Uploaded crop image", use_container_width=True)
    st.success("Image saved successfully.")


if ask_clicked:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            result = run_assistant(question, LANGUAGE_OPTIONS[answer_language_label])

        st.markdown(
            f"""
<div class="answer-box">
    <h3>Answer in {html.escape(result["answer_language_name"])}</h3>
    <div class="answer-content">{html.escape(result["final_answer"])}</div>
</div>
""",
            unsafe_allow_html=True,
        )

