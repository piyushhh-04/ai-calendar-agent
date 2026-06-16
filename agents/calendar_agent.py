from memory import Memory
from router import route_request


class CalendarAgent:

    def __init__(self):

        self.memory = Memory()

        self.system_prompt = """

        You are an AI Calendar Assistant.

        You help users:

        - Create events
        - Modify events
        - Delete events

        Always provide helpful responses.

        """


    def run(self, intent, data):

        self.memory.add_system(
            self.system_prompt
        )

        self.memory.add_user(
            str(data)
        )

        result = route_request(
            intent,
            data
        )

        self.memory.add_assistant(
            str(result)
        )

        return result


    def show_memory(self):

        return self.memory.get_messages()