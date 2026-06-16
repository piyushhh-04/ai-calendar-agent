from tools.calendar import update_event


def modify_event_workflow(
    event_id=None,
    title=None,
    field=None,
    value=None
):

    return update_event(
        event_id=event_id,
        title=title,
        field=field,
        value=value
    )