PERSON_TO_PERSON = "person->person"

ACTIONS = {
    # actor is always taken as one of the values of the actions
    # conditions and effects are specified like name__effect
    "kill": {
        "objects": ["victim"],
        "type": PERSON_TO_PERSON,
        "preconditions": {
            "victim__alive": True,
        },
        "effects": {
            "victim__alive": False,
        }
    }
}

def apply_action(action, agent, **objects):
    if action not in ACTIONS:
        raise ValueError("The action must be defined in the ACTIONS dictionary.")
    