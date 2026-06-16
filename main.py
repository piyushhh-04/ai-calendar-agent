from agents.calendar_agent import CalendarAgent


agent = CalendarAgent()

def main():

    print("Calendar ready. Type 'exit' to quit.")

    try:
        while True:

            user_input = input("You: ").strip()

            if user_input.lower() in {"exit", "quit"}:

                break

            if not user_input:

                continue

            response = agent.run(user_input)

            print(f"Agent: {response}")
    except (KeyboardInterrupt, EOFError):

        print("\nGoodbye.")


if __name__ == "__main__":

    main()