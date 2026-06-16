from dotenv import load_dotenv
import os
import time

import httpx

# Load environment variables
load_dotenv()

def _get_gemini_api_key():

    return os.getenv("GEMINI_API_KEY")


def _messages_to_gemini_payload(messages):

    system_parts = []
    contents = []

    for message in messages:

        role = message.get("role")
        content = message.get("content", "")

        if role == "system":

            system_parts.append(content)

        elif role == "user":

            contents.append({
                "role": "user",
                "parts": [{"text": content}],
            })

        elif role == "assistant":

            contents.append({
                "role": "model",
                "parts": [{"text": content}],
            })

    payload = {"contents": contents}

    if system_parts:

        payload["systemInstruction"] = {
            "parts": [{"text": "\n\n".join(system_parts)}],
        }

    return payload


def _chat_gemini(messages, model, response_format=None):

    api_key = _get_gemini_api_key()

    if not api_key:

            raise RuntimeError(
                "Gemini API key not found. Set GEMINI_API_KEY in your .env file."
            )

    payload = _messages_to_gemini_payload(messages)
    payload["generationConfig"] = {"temperature": 0}

    if response_format is not None:

        payload["generationConfig"]["responseMimeType"] = "application/json"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):

        response = httpx.post(
            url,
            params={"key": api_key},
            json=payload,
            timeout=60,
        )

        if response.status_code == 200:

            data = response.json()

            candidates = data.get("candidates", [])

            if not candidates:

                raise RuntimeError("Gemini returned no candidates.")

            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            return "".join(part.get("text", "") for part in parts)

        if response.status_code == 429 and attempt < max_attempts:

            retry_after = response.headers.get("Retry-After")
            wait_seconds = 5 * attempt

            if retry_after is not None:

                try:

                    wait_seconds = max(wait_seconds, int(float(retry_after)))

                except (TypeError, ValueError):

                    pass

            time.sleep(wait_seconds)
            continue

        raise RuntimeError(
            f"Gemini request failed with status {response.status_code}: {response.text}"
        )


def chat(
    messages,
    model="gemini-2.0-flash",
    response_format=None,
):
    """
    Send messages to the model and return text.
    """

    return _chat_gemini(messages, model, response_format=response_format)