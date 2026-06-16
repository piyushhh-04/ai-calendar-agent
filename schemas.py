from pydantic import BaseModel
from typing import List


class CalendarEvent(BaseModel):

    title: str

    date: str

    start_time: str

    end_time: str

    attendees: List[str] = []


class EventModification(BaseModel):

    event_id: int

    field_to_modify: str

    new_value: str


class EventDeletion(BaseModel):

    event_id: int