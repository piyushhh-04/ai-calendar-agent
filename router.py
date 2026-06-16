from workflows.create_event import create_event_workflow
from workflows.modify_event import modify_event_workflow
from workflows.delete_event import delete_event_workflow
from schemas import IntentClassification


def route_request(request):

    """
    Routes the user request
    to the appropriate workflow.
    """

    if not isinstance(request, IntentClassification):

        request = IntentClassification.model_validate(request)

    intent = request.intent

    if intent == "create":

        if request.event is None:

            return {
                "status": "error",
                "message": "Missing event details"
            }

        return create_event_workflow(request.event.model_dump(exclude_none=True))


    elif intent == "modify":

        return modify_event_workflow(
            event_id=request.event_id,
            title=request.target_event,
            field=request.field_to_modify,
            value=request.new_value
        )


    elif intent == "delete":

        return delete_event_workflow(
            event_id=request.event_id,
            title=request.target_event
        )


    else:

        return {

            "status": "error",

            "message": "Unknown intent"
        }