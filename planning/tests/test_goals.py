import unittest

from planning.agents import Agent
from planning.goals import Goal, generate_goal


class Agent(object):
    def __init__(self, name):
        self._name = name
    alive = True


class TestGenerateGoal(unittest.TestCase):
    def test_generate_goal(self):
        batman = Agent('batman')
        objects = [batman]
        goal = generate_goal(objects)
        self.assertEqual(
            goal,
            (batman, 'alive', False)
        )

    def test_multiple_objects(self):
        batman = Agent('batman')
        robin = Agent('robin')
        robin.alive = False
        objects = [batman, robin]
        goal = generate_goal(objects)
        self.assertIn(
            goal,
            [
                (batman, 'alive', False),
                (robin, 'alive', True)
            ]
        )


class TestGoal(unittest.TestCase):
    def test_init(self):
        """ValueError raised when keywords not specified."""
        self.assertRaises(
            ValueError,
            Goal,
            'boger'
        )

    def test_is_satisfied(self):
        """Test a case where a goal is satisfied."""
        test_obj = Agent("test agent")
        test_obj.alive = False
        test_goal = Goal(
            "victim is dead", obj=test_obj, attr_name='alive', value=False)
        self.assertTrue(test_goal.is_satisfied())

    def test_not_satisfied(self):
        """Test a case where a goal is not satisfied."""
        test_obj = Agent("test agent")
        test_obj.alive = True
        test_goal = Goal(
            "victim is dead", obj=test_obj, attr_name='alive', value=False)
        self.assertFalse(test_goal.is_satisfied())
