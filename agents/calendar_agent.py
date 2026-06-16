from datetime import datetime
from pathlib import Path

from client import chat
from memory import Memory
from router import route_request
from utils.parser import parse_user_input


class CalendarAgent:

    def __init__(self):

        self.memory = Memory()
        self.model = "meta-llama/llama-3.2-3b-instruct:free"
        self.system_prompt = self._load_system_prompt()

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

    def _format_result(self, result, request):

        if not isinstance(result, dict):
            return str(result)

        if result.get("status") != "success":
            return result.get("message", "Something went wrong")

        event = result.get("event") or result.get("deleted") or {}

        if request.intent == "create":
            title = event.get("title", "event")
            date = event.get("date")
            start_time = event.get("start_time")
            end_time = event.get("end_time")
            details = [f'Created "{title}"']

            if date:
                details.append(f"on {date}")

            if start_time:
                if end_time:
                    details.append(f"from {start_time} to {end_time}")
                else:
                    details.append(f"at {start_time}")

            return " ".join(details) + "."

        if request.intent == "modify":
            title = event.get("title", request.target_event or "event")
            return f'Updated "{title}" successfully.'

        if request.intent == "delete":
            title = event.get("title", request.target_event or "event")
            return f'Deleted "{title}" successfully.'

        return result.get("message", "Done")

    def run(self, user_text):

        messages = self._build_messages(user_text)

        llm_response = chat(
            messages=messages,
            model=self.model,
            response_format={"type": "json_object"}
        )

        request = parse_user_input(llm_response)
        result = route_request(request)
        assistant_response = self._format_result(result, request)

        self.memory.add_assistant(assistant_response)
        return assistant_response

    def show_memory(self):

        return self.memory.get_messages()
