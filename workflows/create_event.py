from schemas import CalendarEvent
from tools.calendar import create_event


def create_event_workflow(data: dict):

    """
    Create a CalendarEvent object
    and save it to our fake DB.
    """

    event = CalendarEvent(**data)

    result = create_event(
        event.model_dump()
    )

    return result