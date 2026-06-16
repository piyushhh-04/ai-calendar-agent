from tools.calendar import events_db


def modify_event_workflow(
    event_id,
    field,
    value
):

    if event_id >= len(events_db):

        return {

            "status": "error",

            "message": "Event not found"
        }

    events_db[event_id][field] = value

    return {

        "status": "success",

        "event": events_db[event_id]
    }