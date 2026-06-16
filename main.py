from agents.calendar_agent import CalendarAgent


agent = CalendarAgent()


result = agent.run(

    intent="create",

    data={

        "title": "Dinner with Rahul",

        "date": "2026-06-17",

        "start_time": "20:00",

        "end_time": "22:00",

        "attendees": ["Rahul"]
    }

)


print(result)