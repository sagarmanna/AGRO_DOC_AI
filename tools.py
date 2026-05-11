from __future__ import annotations

import json
import csv
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"


def _load_json(filename: str) -> list[dict]:
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_crop_faq() -> list[dict]:
    return _load_json("crop_faq.json")


def load_disease_info() -> list[dict]:
    return _load_json("disease_info.json")


def load_fertilizer_data() -> list[dict]:
    path = DATA_DIR / "fertilizer_data.csv"
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def search_agriculture_knowledge(query: str) -> str:
    if not query.strip():
        return ""

    query_lower = query.lower()
    matches: list[str] = []

    for item in load_crop_faq():
        text = f"{item.get('question', '')} {item.get('answer', '')}".lower()
        if any(word in text for word in query_lower.split()):
            matches.append(f"FAQ: {item.get('question')}\nAnswer: {item.get('answer')}")

    for item in load_disease_info():
        text = " ".join(str(value) for value in item.values()).lower()
        if any(word in text for word in query_lower.split()):
            matches.append(
                "Disease: {name}\nCrop: {crop}\nSymptoms: {symptoms}\nTreatment: {treatment}".format(
                    name=item.get("name", "Unknown"),
                    crop=item.get("crop", "Unknown"),
                    symptoms=item.get("symptoms", "Not available"),
                    treatment=item.get("treatment", "Not available"),
                )
            )

    fertilizer_data = load_fertilizer_data()
    if fertilizer_data:
        for row in fertilizer_data:
            row_text = " ".join(str(value) for value in row.values()).lower()
            if any(word in row_text for word in query_lower.split()):
                matches.append(
                    "Fertilizer suggestion: Crop {crop}, soil {soil}, fertilizer {fertilizer}, dosage {dosage}".format(
                        crop=row.get("crop", "Unknown"),
                        soil=row.get("soil_type", "Unknown"),
                        fertilizer=row.get("fertilizer", "Unknown"),
                        dosage=row.get("dosage", "Unknown"),
                    )
                )

    if not matches:
        return ""

    return "\n\n".join(matches[:5])
