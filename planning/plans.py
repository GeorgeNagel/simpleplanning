from itertools import permutations

from planning.actions import calculate_effects, calculate_preconditions
from planning.settings import log


class PossiblePlan(object):
    """Helper class to track conditions when searching for plans."""
    conditions = None
    actions_to_perform = None

    def __init__(self):
        self.conditions = {}
        self.actions_to_perform = []

    def matches_initial_conditions(self):
        """Check if a possible plan matches initial conditions.

        PARAMETERS:
        * possible_plan - A PossiblePlan object.
        * actor - The agent planning.
        * objects - A list of possible objects.
        """
        all_conditions_match = True
        for condition in self.conditions:
            obj, attr_name = condition
            attr_value = self.conditions[condition]
            if getattr(obj, attr_name) != attr_value:
                all_conditions_match = False
        return all_conditions_match

    def copy(self):
        """Return a copy PossiblePlan that references the same objects."""
        _copy = PossiblePlan()
        for condition, value in self.conditions.iteritems():
            _copy.conditions[condition] = value
        for action_to_perform in self.actions_to_perform:
            _copy.actions_to_perform.append(action_to_perform)
        return _copy

    def prepend_action(self, action_tuple):
        """Prepend an action to actions_to_perform and update conditions.
        PARAMETERS:
        * action_tuple - A tuple like (actor, action, objects_dict).
        """
        # Prepend the action to the list of actions performed
        self.actions_to_perform = [action_tuple] + self.actions_to_perform

        # Update the conditions for what they would need to be before the
        # action was performed
        actor, action, objects_dict = action_tuple
        preconditions = calculate_preconditions(
            action, actor=actor, **objects_dict
        )
        for precondition in preconditions:
            obj, attr_name, value = precondition
            self.conditions[(obj, attr_name)] = value


def _create_initial_plan(goal):
    """Set up the conditions for the initial_plan."""
    initial_plan = PossiblePlan()
    goal_obj, goal_attr, goal_value = goal
    initial_plan.conditions[(goal_obj, goal_attr)] = goal_value
    return initial_plan


def select_plan(actor=None, goal=None, available_actions=None, objects=None):
    selected_plan = breadth_first_plan_search(
        actor=actor, goal=goal, available_actions=available_actions,
        objects=objects)
    actions_sequence = selected_plan.actions_to_perform
    return actions_sequence


def breadth_first_plan_search(
        actor=None, goal=None, available_actions=None,
        objects=None, possible_plans=None):
    """Perform a breadth-first backwards search from the goal.

    PARAMETERS:
    * actor - The agent planning.
    * goal - A tuple like (object, attr_name, attr_value).
    * available_actions - A list of possible actions.
    * objects - A list of possible objects to act upon.
    * possible_plans - A list of PossiblePlan objects.
    """
    required_keys = [actor, goal, available_actions, objects]
    if any([keywrd is None for keywrd in required_keys]):
        raise ValueError("Inputs must not be None.")

    # Create an empty possible plan if this is the first iteration.
    if not possible_plans:
        possible_plans = [_create_initial_plan(goal)]

    # Check if the goal is satisfied by one of the possible plans.
    for possible_plan in possible_plans:
        log.debug("Plan: %s" % possible_plan)
        if possible_plan.matches_initial_conditions():
            return possible_plan

    next_possible_plans = []
    # Spawn off new possible plans back from existing possible plans
    for possible_plan in possible_plans:
        # Check for actions with effects that match the conditions of
        # the possible plan
        possible_previous_actions = _actions_that_match_possible_plan(
            possible_plan, available_actions=available_actions,
            actor=actor, objects=objects)
        log.debug("Posssible actions: %s" % possible_previous_actions)

        for possible_previous_action in possible_previous_actions:
            # Spawn a copied version of the plan to modify with the
            next_possible_plan = possible_plan.copy()
            next_possible_plan.prepend_action(possible_previous_action)
            next_possible_plans.append(next_possible_plan)

    return breadth_first_plan_search(
        actor=actor, goal=goal, available_actions=available_actions,
        objects=objects, possible_plans=next_possible_plans)


def _actions_that_match_possible_plan(
        possible_plan, available_actions=None, actor=None, objects=None):
    """Return a list of actions.

    The actions returned have effects that match the
    conditions of possible_plan.

    PARAMETERS:
    * possible_plan - A PossiblePlan object.
    * available_actions - A list of actions.
    * actor - The agent planning.
    * objects - A list of possible objects to act upon.
    """
    possible_previous_actions = []
    for action in available_actions:
        log.debug("Action: %s" % action)
        number_of_objects = len(action['objects'])
        # Permute over all possible objects for the action
        log.debug("objects: %s" % repr(objects))
        log.debug("nobjects; %s" % repr(number_of_objects))
        for tuple_of_objects in permutations(objects, number_of_objects):
            log.debug("TUP: %s" % repr(tuple_of_objects))
            objects_dict = {}
            for obj_name, obj in zip(action['objects'], tuple_of_objects):
                objects_dict[obj_name] = obj
            log.debug("OBJ Dict: %s" % objects_dict)
            action_matches = _action_effects_match_possible_plan(
                action, possible_plan, actor, **objects_dict)
            if action_matches:
                log.debug("MATCH")
                possible_previous_actions.append(
                    (actor, action, objects_dict)
                )
    return possible_previous_actions


def _action_effects_match_possible_plan(
        action, possible_plan=None, actor=None, **objects):
    action_effects = calculate_effects(
        action, actor=actor, **objects
    )
    log.debug("Actions effects: %s" % action_effects)
    # No effects may contradict conditions of the possible plan
    # but at least some of the effects should match
    all_effects_match = True
    some_effects_match = False
    for condition in action_effects:
        value = action_effects[condition]
        if condition in possible_plan.conditions:
            if possible_plan.conditions[condition] != value:
                # An effect of this action does not match
                # the conditions of the possible plan
                all_effects_match = False
            some_effects_match = True
    action_matches = (all_effects_match and some_effects_match)
    return action_matches
