import unittest

from planning.plans import (
    select_plan, breadth_first_plan_search, PlanHistory,
    _history_satisfies_goal, _update_history_with_action)


class Agent(object):
    def __init__(self, name):
        self._name = name
    alive = True
    has_sword = False

    def __repr__(self):
        """Helpful method for using repr() when debugging."""
        return '<' + self._name + '>'

# Test actions
get_sword = {
    "objects": [],
    "preconditions": {
        "agent__has_sword": False,
    },
    "effects": {
        "agent__has_sword": True,
    }
}

kill = {
    "objects": ["victim"],
    "preconditions": {
        "victim__alive": True,
        "agent__has_sword": True,
    },
    "effects": {
        "victim__alive": False,
    }
}


class TestPlanning(unittest.TestCase):
    def setUp(self):
        self.knight = Agent('Knight')
        self.dragon = Agent('Dragon')
        self.possible_actions = [kill, get_sword]
        self.knight_goal = (self.dragon, 'alive', False)
        self.objects = [self.knight, self.dragon]

    def test_planning(self):
        selected_plan = select_plan(
            self.knight, self.knight_goal, self.possible_actions, self.objects
        )
        self.assertEqual(
            selected_plan,
            [
                (get_sword, {}),
                (kill, {'victim': self.dragon}),
            ]
        )


class TestBreadthFirstPlanSearch(unittest.TestCase):
    def setUp(self):
        self.knight = Agent('Knight')
        self.dragon = Agent('Dragon')
        self.possible_actions = [kill, get_sword]
        self.knight_goal = (self.dragon, 'alive', False)
        self.objects = [self.knight, self.dragon]

    def test_goal_already_met(self):
        """Ensure that a history is returned when it satisfies the goal."""
        plan_history = PlanHistory()
        plan_history.conditions = {(self.dragon, 'alive'): False}
        plan_history.actions_performed = [
            (self.knight, kill, {'victim': self.dragon})
        ]

        selected_plan_history = breadth_first_plan_search(
            self.knight, self.knight_goal, self.possible_actions,
            self.objects, [plan_history]
        )
        self.assertEqual(selected_plan_history, plan_history)

    def test_breadth_first_plan_search(self):
        """Test the breadth-first plan search algorithm."""
        # Shortcut so that there is only one action needed
        self.knight.has_sword = True
        selected_history = breadth_first_plan_search(
            self.knight, self.knight_goal, self.possible_actions,
            self.objects, [])
        print "SELECTED HISTORY: %s" % repr(selected_history)
        self.assertEqual(
            selected_history.actions_performed,
            [(self.knight, kill, {'victim': self.dragon})]
        )


class PlanHistorySatisfiesGoalTest(unittest.TestCase):
    """Test a PlanHistory that satisfies a goal."""
    def test_history_satisfies(self):
        dragon = Agent('dragon')
        plan_history = PlanHistory()
        plan_history.conditions = {(dragon, 'alive'): False}
        goal = (dragon, 'alive', False)
        self.assertTrue(
            _history_satisfies_goal(plan_history, goal)
        )

    def test_history_doesnt_satisfy(self):
        """Test a PlanHistory that does not satisfy a goal."""
        # Are you ever satisfied? No, I'm never satisfied.
        dragon = Agent('dragon')
        plan_history = PlanHistory()
        plan_history.conditions = {(dragon, 'alive'): True}
        goal = (dragon, 'alive', False)
        self.assertFalse(
            _history_satisfies_goal(plan_history, goal)
        )


class TestUpdatePlanHistoryWithAction(unittest.TestCase):
    def test_update_history_with_action(self):
        plan_history = PlanHistory()
        knight = Agent('Knight')
        dragon = Agent('Dragon')
        plan_history.conditions = {(knight, 'alive'): True}
        _update_history_with_action(
            plan_history, knight, kill, {'victim': dragon})
        self.assertEqual(
            plan_history.conditions,
            {
                (knight, 'alive'): True,
                (dragon, 'alive'): False,
            }
        )
