events_db = []


def _normalize_text(value):

    return str(value).strip().lower()


def _find_event_index(event_id=None, title=None):

    if event_id is not None:

        for index, event in enumerate(events_db):

            if event.get("event_id") == event_id:

                return index

    if title:

        normalized_title = _normalize_text(title)

        for index, event in enumerate(events_db):

            current_title = _normalize_text(event.get("title", ""))

            if (
                current_title == normalized_title
                or normalized_title in current_title
                or current_title in normalized_title
            ):

                return index

    return None


def create_event(event):

    stored_event = dict(event)

    stored_event["event_id"] = stored_event.get("event_id", len(events_db))

    events_db.append(stored_event)

    return {
        "status": "success",
        "message": "Event created",
        "event": stored_event
    }


def update_event(event_id=None, title=None, field=None, value=None):

    index = _find_event_index(event_id=event_id, title=title)

    if index is None:

        return {
            "status": "error",
            "message": "Event not found"
        }

    if not field:

        return {
            "status": "error",
            "message": "No field provided to modify"
        }

    events_db[index][field] = value

    return {
        "status": "success",
        "message": "Event updated",
        "event": events_db[index]
    }


def delete_event(event_id=None, title=None):

    index = _find_event_index(event_id=event_id, title=title)

    if index is not None:

        deleted = events_db.pop(index)

        return {
            "status": "success",
            "deleted": deleted
        }

    return {
        "status": "error",
        "message": "Event not found"
    }