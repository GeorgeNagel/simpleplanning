from itertools import permutations
import random

from planning.settings import log


class Goal(object):
    """Utility class for goals."""
    # TODO: Allow for multiple subgoals
    name = ""
    # A condition instance
    _goal_condition = None
    _goal_value = None

    def __init__(self, name, condition=None, value=None):
        if any(val is None for val in [condition, value]):
            raise ValueError("Must specify condition, and value")
        self.name = name
        self._goal_condition = condition
        self._goal_value = value

    def __repr__(self):
        return "<%s: %s>" % (
            self._goal_condition, self._goal_value
        )

    @property
    def goal_condition(self):
        return self._goal_condition

    @property
    def goal_value(self):
        return self._goal_value

    def is_satisfied(self):
        """Check if a goal is currently satisfied."""
        actual_value = self._goal_condition.evaluate()
        return actual_value == self._goal_value


def generate_goal(conditions, objects):
    """Returns a Goal object.
    PARAMETERS:
    * conditions - A list of Condition classes.
    * objects - A list of objects on which the conditions could be calculated.

    Note: Currently assumes that all objects can be used with all conditions.
    """
    log.debug("Generating goal.")
    # Select a random condition
    selected_condition = random.choice(conditions)
    # Select a random set of objects for the condition
    number_of_objects = selected_condition.number_of_objects
    object_tuples = [tup for tup in permutations(objects, number_of_objects)]
    object_tuple = random.choice(object_tuples)
    object_list = list(object_tuple)
    # Get the current value of the condition
    condition_instance = selected_condition(object_list)
    current_value = condition_instance.evaluate()
    goal_value = not current_value
    goal = Goal("random goal", condition_instance, goal_value)
    return goal
