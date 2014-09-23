from itertools import permutations

from planning.actions import check_preconditions, calculate_effects
from planning.settings import log


class PlanHistory(object):
    """Helper class to track conditions as they are effected by actions."""
    # Dictionary with keys (object, attribute_name), values of condition value.
    conditions = None
    actions_performed = None

    def __init__(self):
        self.conditions = {}
        self.actions_performed = []

    def __repr__(self):
        """Helper method for debugging."""
        return "<Plan History> Conditions: %s. Actions Performed: %s" % (
            self.conditions, self.actions_performed
        )

    def copy(self):
        copy = PlanHistory()
        for condition in self.conditions:
            copy.conditions[condition] = self.conditions[condition]
        for action_performed in self.actions_performed:
            copy.actions_performed.append(action_performed)
        return copy


def select_plan(agent, goal, possible_actions, objects):
    """Generate a plan that satisfies the agent's goals."""
    log.debug("Selecting plan")
    valid_plan_history = breadth_first_plan_search(
        agent, goal, possible_actions, objects, []
    )
    return valid_plan_history


def breadth_first_plan_search(
        agent, goal, possible_actions, objects, histories):
    """Perform a breadth-first search of the action space for the agent's goal.
    PARAMETERS:
    * agent - the agent who is planning.
    * goal - the goal of the plan. A tuple (agent, attribute, value).
    * possible_actions - a list of action dictionaries.
    * objects - a list of objects on which actions can be performed.
    * histories - a list of PlanHistory objects containing
        information about the prior round of the breadth-first search.
    """
    # Check if one of the previous round of possible
    # actions satisfied the goal.
    for history in histories:
        if _history_satisfies_goal(history, goal):
            log.debug("History satsified: %s" % history)
            return history
        log.debug("Here after I returned")
    if not histories:
        # This is the first round of planning. Populate an empty PlanHistory
        histories = [PlanHistory()]
    next_round_histories = []
    # Iterate over prior-round searches, creating new possible histories
    for history in histories:
        log.debug("History: %s" % repr(history))
        log.debug("Possible Actions: %s" % repr(possible_actions))
        for action in possible_actions:
            log.debug("Action: %s" % repr(action))
            number_of_objects_in_action = len(action['objects'])
            if number_of_objects_in_action == 0:
                action_is_valid = check_preconditions(action, agent)
                objects_dict = {}
                if action_is_valid:
                    # Create a new history with
                    next_history = history.copy()
                    _update_history_with_action(
                        next_history, agent, action, objects_dict)
                    next_round_histories.append(next_history)
                    log.debug("Updated history: %s" % repr(next_history))
            else:
                for combination_of_objects in permutations(
                        objects, number_of_objects_in_action):
                    log.debug("Combination: %s" % repr(combination_of_objects))

                    # Add any valid action-object permutations
                    # as possible histories.

                    # Dict to specify keyword arguments for actions
                    objects_dict = {}
                    for obj_name, obj in zip(
                            action['objects'], combination_of_objects):
                        log.debug("key, val: %s" % repr((obj_name, obj)))
                        objects_dict[obj_name] = obj
                        action_is_valid = check_preconditions(
                            action, agent, **objects_dict)
                        if action_is_valid:
                            # Create a new history with
                            next_history = history.copy()
                            _update_history_with_action(
                                next_history, agent, action, objects_dict)
                            next_round_histories.append(next_history)
                            log.debug("Updated history: %s" % repr(next_history))

    log.debug("Continuing search")
    # Continue search at the next depth level
    return breadth_first_plan_search(
        agent, goal, possible_actions, objects, next_round_histories
    )


def _update_history_with_action(history, agent, action, objects_dict):
    """Modify a PlanHistory in-place to update it with an applied action."""
    action_effects = calculate_effects(action, agent=agent, **objects_dict)
    history.conditions.update(action_effects)
    history.actions_performed.append((agent, action, objects_dict))


def _history_satisfies_goal(history, goal):
    for attribute_tuple in history.conditions:
        # Unpack the object, attribute, and value
        obj, attr_name = attribute_tuple
        val = history.conditions[attribute_tuple]

        if goal == (obj, attr_name, val):
            return True
    return False
