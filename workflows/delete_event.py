from tools.calendar import delete_event


def delete_event_workflow(event_id=None, title=None):

    result = delete_event(event_id=event_id, title=title)

    return result