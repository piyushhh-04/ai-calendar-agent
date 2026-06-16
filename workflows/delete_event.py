from tools.calendar import delete_event


def delete_event_workflow(event_id):

    result = delete_event(event_id)

    return result