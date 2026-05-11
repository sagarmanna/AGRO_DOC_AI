from __future__ import annotations

import os

from dotenv import load_dotenv
import requests


load_dotenv()

try:
    import streamlit as st
except Exception:  # pragma: no cover
    st = None


SYSTEM_PROMPT = """You are AGRO-DOC Smart Assistant, a practical agriculture helper for farmers.
Give clear, safe, friendly, and detailed advice that a farmer can act on.
Use the user's real question only. Do not invent local database facts, fake examples, or sample records.
Prefer this response style:
1. Start with a short direct answer.
2. Give likely causes or diagnosis if relevant.
3. Give practical step-by-step actions.
4. Mention what to avoid.
5. Add warning signs that need urgent local expert help.
6. Ask for missing details such as crop, location, soil, weather, crop age, symptoms, or image details.
Keep pesticide, fertilizer, and dosage advice cautious. Do not give exact chemical dosage unless the user provides enough context and local expert verification is recommended.
Use simple words, short paragraphs, and bullet points when helpful.
If the question is missing crop, location, soil, weather, image details, or symptoms needed for a safe answer, still give general safe guidance, then ask for those details.
Recommend checking with a local agriculture expert for severe disease, pesticide use, fertilizer dosage, or region-specific regulation.
"""


def _fallback_answer() -> str:
    return (
        "I could not reach the AI service, so I cannot generate a full LLM answer right now. "
        "Please check your API key, model access, and internet connection, then try again."
    )


def _extract_response_text(data: dict) -> str:
    if data.get("output_text"):
        return str(data["output_text"])

    output_parts: list[str] = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                output_parts.append(str(content["text"]))

    return "\n".join(output_parts).strip()


def _setting(name: str, default: str = "") -> str:
    value = os.getenv(name, "").strip()
    if value:
        return value

    if st is not None:
        try:
            secret_value = st.secrets.get(name, "")
            if secret_value:
                return str(secret_value).strip()
        except Exception:
            pass

    return default


def ask_agro_agent(question: str, response_language: str = "English") -> str:
    api_key = _setting("OPENAI_API_KEY")

    if not api_key or api_key == "your_openai_api_key_here":
        return _fallback_answer()

    model = _setting("OPENAI_MODEL", "gpt-5.4-mini")
    payload = {
        "model": model,
        "input": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"User question:\n{question}\n\n"
                    f"Answer in {response_language}. "
                    "Make the answer user-friendly, detailed, practical, and easy for a farmer to understand. "
                    "Use headings or bullets where useful."
                ),
            },
        ],
        "reasoning": {"effort": _setting("OPENAI_REASONING_EFFORT", "low")},
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=45,
        )
        response.raise_for_status()
        data = response.json()
        answer = _extract_response_text(data)
        if answer:
            return answer
        return "The AI service responded, but no answer text was returned."
    except Exception as exc:
        return f"{_fallback_answer()}\n\nTechnical detail: {exc}"
