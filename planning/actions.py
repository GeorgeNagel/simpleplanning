from planning.settings import log

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


def apply_action(action, actor=None, **objects):
    if not check_preconditions(action, actor=actor, **objects):
        raise ValueError(
            "Preconditions not passed."
        )

    # Dict of all objects (including the actor)
    all_objects = {'actor': actor}
    all_objects.update(objects)

    for effect in action['effects']:
        # Split the effect into the object and its attribute
        obj_name, attr_name = effect.split("__")
        obj = all_objects[obj_name]
        effect_value = action['effects'][effect]
        setattr(obj, attr_name, effect_value)


def calculate_effects(action, actor=None, **objects):
    """Calculate the effects tuple for planning activities."""
    calculated_effects = {}
    for action_effect in action['effects']:
        # Parse the effect condition/value pair
        obj_name, attr_name = action_effect.split('__')
        effect_value = action['effects'][action_effect]

        # Find the actual object by name in the objects dict
        # Include the actor in the list of objects
        objects.update({'actor': actor})
        obj = objects[obj_name]

        calculated_effects[(obj, attr_name)] = effect_value
    return calculated_effects


def calculate_preconditions(action, actor=None, **objects):
    """Create the list of preconditions tuples like (obj, attr_name, value)."""
    all_objects = {'actor': actor}
    all_objects.update(objects)

    preconditions_tuples = []
    for precondition in action['preconditions']:
        # Split the precondition into the object and its attribute
        obj_name, attr_name = precondition.split("__")
        obj = all_objects[obj_name]
        precondition_value = action['preconditions'][precondition]
        preconditions_tuple = (obj, attr_name, precondition_value)
        preconditions_tuples.append(preconditions_tuple)
    return preconditions_tuples


def check_preconditions(action, actor=None, **objects):
    # Dict of all objects (including the actor)
    log.debug("Checking preconditions")
    log.debug("action: %s, actor: %s, objects: %s" % (
        action, actor, objects))
    all_objects = {'actor': actor}
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
    log.debug("Preconditions met? %s" % all_preconditions_met)
    return all_preconditions_met
