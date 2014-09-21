class History(object):
    conditions = None
    actions_performed = None

    def __init__(self):
        self.conditions = []
        self.actions_performed = []


def select_plan(agent, goal, possible_actions, objects):
    """Generate a plan that satisfies the agent's goals."""
    valid_history = breadth_first_plan_search(
        agent, goal, possible_actions, objects, []
    )


def breadth_first_plan_search(
        agent, goal, possible_actions, objects, histories):
    """Perform a breadth-first search of the action space for the agent's goal.
    PARAMETERS:
    * agent - the agent who is planning.
    * goal - the goal of the plan. A tuple (agent, attribute, value).
    * possible_actions - a list of action dictionaries.
    * objects - a list of objects on which actions can be performed.
    * histories - a list of History objects containing information about the
        prior round of the breadth-first search.
    """
    # Check if one of the previous round of possible
    # actions satisfied the goal.
    for history in histories:
        if _history_satisfies_goal(history, goal):
            return history
    if not histories:
        # Test the first round of actions
        for action in possible_actions:
            pass


def _history_satisfies_goal(history, goal):
    for condition in history.conditions:
        if goal == condition:
            return True
    return False
