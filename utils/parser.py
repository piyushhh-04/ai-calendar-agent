"""Parser helpers for validating structured model output."""

import json

from schemas import IntentClassification


def parse_user_input(text):
    """
    Convert JSON text from the LLM into a validated intent object.
    """

    cleaned = text.strip()

    if cleaned.startswith("```"):

        cleaned = cleaned.strip("`")

        if cleaned.startswith("json"):

            cleaned = cleaned[4:].strip()

    start_index = cleaned.find("{")

    end_index = cleaned.rfind("}")

    if start_index != -1 and end_index != -1:

        cleaned = cleaned[start_index : end_index + 1]

    data = json.loads(cleaned)

    return IntentClassification.model_validate(data)