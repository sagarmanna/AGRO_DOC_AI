from __future__ import annotations

from dataclasses import dataclass

try:
    from deep_translator import GoogleTranslator
    from langdetect import detect
except Exception:  # pragma: no cover
    GoogleTranslator = None
    detect = None


@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str


LANGUAGE_OPTIONS = {
    "Auto detect": "auto",
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Urdu": "ur",
}

LANGUAGE_NAMES = {code: name for name, code in LANGUAGE_OPTIONS.items() if code != "auto"}


class TranslatorService:
    def __init__(self) -> None:
        self._translator_available = bool(GoogleTranslator and detect)

    def to_english(self, text: str) -> TranslationResult:
        cleaned = text.strip()
        if not cleaned:
            return TranslationResult(text, "", "en")

        if not self._translator_available:
            return TranslationResult(cleaned, cleaned, "en")

        source_language = "en"
        try:
            source_language = detect(cleaned) or "en"
        except Exception:
            pass

        if source_language == "en":
            return TranslationResult(cleaned, cleaned, "en")

        try:
            translated = GoogleTranslator(source=source_language, target="en").translate(cleaned)
            return TranslationResult(cleaned, translated, source_language)
        except Exception:
            return TranslationResult(cleaned, cleaned, source_language)

    def from_english(self, text: str, target_language: str) -> str:
        if target_language == "auto":
            target_language = "en"

        if not text.strip() or target_language == "en" or not self._translator_available:
            return text

        try:
            return GoogleTranslator(source="en", target=target_language).translate(text)
        except Exception:
            return text


def language_name(language_code: str) -> str:
    return LANGUAGE_NAMES.get(language_code, language_code)
