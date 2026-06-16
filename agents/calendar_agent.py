from datetime import datetime
from pathlib import Path
import json

from client import chat
from memory import Memory
from tools.calendar import create_event, delete_event, update_event


class CalendarAgent:

    def __init__(self):

        self.memory = Memory()
        self.model = self._select_model()
        self.system_prompt = self._load_system_prompt()

    def _select_model(self):

        return "nex-agi/nex-n2-pro:free"

    def _load_system_prompt(self):

        prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "system_prompt.txt"
        base_prompt = prompt_path.read_text(encoding="utf-8").strip()
        today = datetime.now().date().isoformat()

        return f"{base_prompt}\n\nToday is {today}."

    def _build_messages(self, user_text):

        if not self.memory.get_messages():
            self.memory.add_system(self.system_prompt)

        self.memory.add_user(user_text)
        return self.memory.get_messages()

    def _parse_request(self, llm_response):

        cleaned = llm_response.strip()

        if cleaned.startswith("```"):

            cleaned = cleaned.strip("`")

            if cleaned.startswith("json"):

                cleaned = cleaned[4:].strip()

        start_index = cleaned.find("{")
        end_index = cleaned.rfind("}")

        if start_index != -1 and end_index != -1:

            cleaned = cleaned[start_index : end_index + 1]

        return json.loads(cleaned)

    def _create_response(self, event):

        result = create_event(event)
        stored_event = result.get("event", {})
        title = stored_event.get("title", "event")
        date = stored_event.get("date")
        start_time = stored_event.get("start_time")
        end_time = stored_event.get("end_time")

        parts = [f'Created "{title}"']

        if date:

            parts.append(f"on {date}")

        if start_time:

            if end_time:

                parts.append(f"from {start_time} to {end_time}")

            else:

                parts.append(f"at {start_time}")

        return " ".join(parts) + "."

    def _modify_response(self, request):

        result = update_event(
            event_id=request.get("event_id"),
            title=request.get("target_event"),
            field=request.get("field_to_modify"),
            value=request.get("new_value"),
        )

        if result.get("status") != "success":

            return result.get("message", "Could not update that event.")

        event = result.get("event", {})
        return f'Updated "{event.get("title", request.get("target_event", "event"))}" successfully.'

    def _delete_response(self, request):

        result = delete_event(
            event_id=request.get("event_id"),
            title=request.get("target_event"),
        )

        if result.get("status") != "success":

            return result.get("message", "Could not delete that event.")

        deleted = result.get("deleted", {})
        return f'Deleted "{deleted.get("title", request.get("target_event", "event"))}" successfully.'

    def run(self, user_text):

        messages = self._build_messages(user_text)

        try:
            llm_response = chat(
                messages=messages,
                model=self.model,
                response_format={"type": "json_object"}
            )
            request = self._parse_request(llm_response)
        except Exception:
            assistant_response = "I couldn\'t understand that. Try again with a date, time, and a short event name."
            self.memory.add_assistant(assistant_response)
            return assistant_response

        intent = request.get("intent")

        if intent == "create":

            assistant_response = self._create_response(request.get("event", {}))

        elif intent == "modify":

            assistant_response = self._modify_response(request)

        elif intent == "delete":

            assistant_response = self._delete_response(request)

        else:

            assistant_response = "I couldn\'t understand that request."

        self.memory.add_assistant(assistant_response)
        return assistant_response

    def show_memory(self):

        return self.memory.get_messages()
