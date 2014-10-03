import random

from planning.settings import log


class Goal(object):
    """Utility class for goals."""
    # TODO: Allow for multiple subgoals
    name = ""
    _goal_all_objects_dict = None
    # A condition instance
    _goal_condition = None
    _goal_value = None

    def __init__(self, name, all_objects_dict=None,
                 condition=None, value=None):
        if any(val is None for val in [all_objects_dict, condition, value]):
            raise ValueError(
                "Must specify all_objects_dict, condition, and value")
        self.name = name
        self._goal_all_objects_dict = all_objects_dict
        self._goal_condition = condition
        self._goal_value = value

    def __repr__(self):
        return "<%s %s: %s>" % (
            self._goal_condition, self._goal_all_objects_dict, self._goal_value
        )

    @property
    def _goal_all_objects_dict(self):
        return self._goal_all_objects_dict

    @property
    def goal_condition(self):
        return self._goal_condition

    @property
    def goal_value(self):
        return self._goal_value

    def is_satisfied(self):
        """Check if a goal is currently satisfied."""
        actual_value = condition.evaluate(**all_objects_dict)
        return actual_value == self._goal_value


def generate_goal(conditions, objects):
    """Returns a Goal object."""
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
