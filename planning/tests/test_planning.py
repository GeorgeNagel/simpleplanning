import unittest

from planning.plans import (
    select_plan, breadth_first_plan_search, History,
    _history_satisfies_goal)


class Agent(object):
    def __init__(self, name):
        self._name = name
    alive = True
    has_sword = False

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
        history = History()
        history.conditions = [(self.dragon, 'alive', False)]
        history.actions_performed = [
            (self.knight, kill, {'victim': self.dragon})
        ]

        selected_history = breadth_first_plan_search(
            self.knight, self.knight_goal, self.possible_actions,
            self.objects, [history]
        )
        self.assertEqual(selected_history, history)

    def test_breadth_first_search(self):
        self.knight.has_sword = True
        selected_history = breadth_first_plan_search(
            self.knight, self.knight_goal, self.possible_actions,
            self.objects, [])
        self.assertEqual(
            selected_history.actions_performed,
            [(self.knight, kill, {'victim': self.dragon})]
        )


class HistorySatisfiesGoalTest(unittest.TestCase):
    """Test a history that satisfies a goal."""
    def test_history_satisfies(self):
        dragon = Agent('dragon')
        history = History()
        history.conditions = [(dragon, 'alive', False)]
        goal = (dragon, 'alive', False)
        self.assertTrue(
            _history_satisfies_goal(history, goal)
        )

    def test_history_doesnt_satisfy(self):
        """Test a history that does not satisfy a goal."""
        # Are you ever satisfied? No, I'm never satisfied.
        dragon = Agent('dragon')
        history = History()
        history.conditions = [(dragon, 'alive', True)]
        goal = (dragon, 'alive', False)
        self.assertFalse(
            _history_satisfies_goal(history, goal)
        )
