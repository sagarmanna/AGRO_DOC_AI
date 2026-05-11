from __future__ import annotations

from agents import ask_agro_agent
from translator import TranslatorService, language_name


translator = TranslatorService()


def run_assistant(user_text: str, answer_language: str = "auto") -> dict[str, str]:
    translated = translator.to_english(user_text)
    target_language = translated.source_language if answer_language == "auto" else answer_language
    target_language_name = language_name(target_language)
    llm_answer = ask_agro_agent(translated.translated_text, target_language_name)

    return {
        "source_language": translated.source_language,
        "source_language_name": language_name(translated.source_language),
        "answer_language": target_language,
        "answer_language_name": target_language_name,
        "english_question": translated.translated_text,
        "llm_answer": llm_answer,
        "final_answer": llm_answer,
    }
