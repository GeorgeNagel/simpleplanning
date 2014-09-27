import random

from planning.settings import log


class Goal(object):
    """Utility class for goals."""
    # TODO: Allow for multiple subgoals
    name = ""
    _goal_obj = None
    _goal_attr_name = None
    _goal_value = None

    def __init__(self, name, obj=None, attr_name=None, value=None):
        if any(val is None for val in [obj, attr_name, value]):
            raise ValueError("Must specify obj, attr_name, and value")
        self.name = name
        self._goal_obj = obj
        self._goal_attr = attr_name
        self._goal_value = value

    def is_satisfied(objects):
        """Check if a goal is currently satisfied."""
        return True


def generate_goal(objects):
    """
    Returns an object, attribute, value pair.
    Assumes that all attributes can be modified by actions.
    Assumes all attributes are boolean.
    """
    log.debug("Generating goal.")
    possible_tuples = []
    for obj in objects:
        public_props = (name for name in dir(obj) if not name.startswith('_'))
        for public_prop in public_props:
            value = getattr(obj, public_prop)
            possible_tuples.append((obj, public_prop, not value))
    # Select a random one.
    selected_goal_tuple = random.choice(possible_tuples)
    return selected_goal_tuple


def goal_satisfied(goal, objects):
    """Check if a goal is currently satisfied."""
    pass
