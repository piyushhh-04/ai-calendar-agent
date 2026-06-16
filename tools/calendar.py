events_db = []


def create_event(event):

    events_db.append(event)

    return {
        "status": "success",
        "message": "Event created",
        "event": event
    }


def get_events():

    return events_db


def delete_event(event_id):

    global events_db

    if event_id < len(events_db):

        deleted = events_db.pop(event_id)

        return {
            "status": "success",
            "deleted": deleted
        }

    return {
        "status": "error",
        "message": "Event not found"
    }