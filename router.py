from workflows.create_event import create_event_workflow
from workflows.modify_event import modify_event_workflow
from workflows.delete_event import delete_event_workflow


def route_request(intent, data):

    """
    Routes the user request
    to the appropriate workflow.
    """

    if intent == "create":

        return create_event_workflow(data)


    elif intent == "modify":

        return modify_event_workflow(

            event_id=data["event_id"],

            field=data["field"],

            value=data["value"]
        )


    elif intent == "delete":

        return delete_event_workflow(

            event_id=data["event_id"]
        )


    else:

        return {

            "status": "error",

            "message": "Unknown intent"
        }