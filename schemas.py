from pydantic import BaseModel
from pydantic import Field
from typing import List, Literal


class CalendarEvent(BaseModel):

    event_id: int | None = None

    title: str

    date: str | None = None

    start_time: str | None = None

    end_time: str | None = None

    attendees: List[str] = Field(default_factory=list)

    notes: str | None = None


class IntentClassification(BaseModel):

    intent: Literal["create", "modify", "delete"]

    event: CalendarEvent | None = None

    target_event: str | None = None

    event_id: int | None = None

    field_to_modify: str | None = None

    new_value: str | None = None

    user_message: str | None = None