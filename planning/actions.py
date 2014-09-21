ACTIONS = {
    # actor is always taken as one of the values of the actions
    # conditions and effects are specified like name__effect
    "kill": {
        "objects": ["victim"],
        "preconditions": {
            "victim__alive": True,
        },
        "effects": {
            "victim__alive": False,
        }
    }
}


def apply_action(action, agent=None, **objects):
    if not check_preconditions(action, agent, **objects):
        raise ValueError(
            "Preconditions not passed."
        )

    # Dict of all objects (including the agent)
    all_objects = {'agent': agent}
    all_objects.update(objects)

    for effect in action['effects']:
        # Split the effect into the object and its attribute
        obj_name, attr_name = effect.split("__")
        obj = all_objects[obj_name]
        effect_value = action['effects'][effect]
        setattr(obj, attr_name, effect_value)


def check_preconditions(action, agent, **objects):
    # Dict of all objects (including the agent)
    all_objects = {'agent': agent}
    all_objects.update(objects)

    # The object arguments must match those required by the preconditions
    if set(objects.keys()) != set(action['objects']):
        raise ValueError(
            "Input objects and action objects mismatch."
            " Input objects: %s. Output objects: %s." % (
                set(objects.keys()), set(action['objects'])
            )
        )

    # Check all the preconditions
    all_preconditions_met = True
    for precondition in action['preconditions']:
        # Split the precondition into the object and its attribute
        obj_name, attr_name = precondition.split("__")
        obj = all_objects[obj_name]
        precondition_value = action['preconditions'][precondition]
        actual_value = getattr(obj, attr_name)

        if precondition_value != actual_value:
            all_preconditions_met = False
            break
    return all_preconditions_met
