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
        self._goal_attr_name = attr_name
        self._goal_value = value

    def __repr__(self):
        return "<%s.%s:%s>" % (
            self._goal_obj, self._goal_attr_name, self._goal_value
        )

    @property
    def goal_obj(self):
        return self._goal_obj

    @property
    def goal_attr_name(self):
        return self._goal_attr_name

    @property
    def goal_value(self):
        return self._goal_value

    def is_satisfied(self):
        """Check if a goal is currently satisfied."""
        actual_value = getattr(self._goal_obj, self._goal_attr_name)
        return actual_value == self._goal_value


def generate_goal(objects):
    """
    Returns an object, attribute, value pair.
    Assumes that all attributes can be modified by actions.
    Assumes all attributes are boolean.
    """
    log.debug("Generating goal.")
    possible_goals = []
    for obj in objects:
        public_properties = [
            name for name in dir(obj) if not name.startswith('_')
        ]
        for public_property in public_properties:
            value = getattr(obj, public_property)
            possible_goals.append(
                Goal(
                    "random goal", obj=obj,
                    attr_name=public_property, value=(not value)
                )
            )
    # Select a random one.
    selected_goal = random.choice(possible_goals)
    return selected_goal
