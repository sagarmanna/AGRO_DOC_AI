# AGRO-DOC Smart Assistant

A Streamlit agriculture assistant that accepts questions in many languages, translates them to English, asks the LLM, and translates the final answer back to the user's language.

## Live App

Open the deployed app here:

https://agrodocaiassist.streamlit.app/

## Project Features

- AI-powered farming question answering
- Multilingual question support with automatic language detection
- Answers in the user's selected or detected language
- Farmer-friendly detailed guidance with practical steps
- Crop disease, fertilizer, irrigation, weather, soil health, and farming scheme question support
- Optional crop image upload for user context
- Modern Streamlit dashboard UI
- Custom AGRO-DOC AI branding and logo
- OpenAI Responses API integration
- Streamlit Cloud deployment support with secure secrets

## Project Flow

```text
User asks in any language
        |
translator.py detects/translates input to English
        |
agents.py sends query to LLM
        |
agents.py uses the real user prompt with the LLM
        |
translator.py converts answer back to user language
        |
app.py shows final response
```

## Setup

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Add your real API key to `.env`.

This version uses `requests` for the OpenAI API call to avoid dependency conflicts with `googletrans`.

## Run

```powershell
streamlit run app.py
```

## Deploy

Deployed app:

https://agrodocaiassist.streamlit.app/

Use Streamlit Community Cloud:

1. Push this repo to GitHub.
2. Create a new Streamlit app from the GitHub repo.
3. Set the main file path to `app.py`.
4. Add these secrets in Streamlit Cloud:

```toml
OPENAI_API_KEY = "your_openai_api_key_here"
OPENAI_MODEL = "gpt-5.4-mini"
OPENAI_REASONING_EFFORT = "low"
```

Do not commit `.env`.
