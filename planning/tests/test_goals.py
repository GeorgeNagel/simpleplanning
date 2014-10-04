import unittest

from planning.agents import Agent
from planning.conditions import Condition
from planning.goals import Goal, generate_goal


# Test Condition
class IsHungry(Condition):
    name = 'is hungry'
    number_of_objects = 1

    def evaluate(self):
        eater_obj = self.objects[0]
        if hasattr(eater_obj, 'is_hungry'):
            return eater_obj.is_hungry
        else:
            return False


class TestGenerateGoal(unittest.TestCase):
    def test_generate_goal(self):
        batman = Agent('batman')
        objects = [batman]
        conditions = [IsHungry]
        goal = generate_goal(conditions, objects)
        self.assertIsInstance(goal._goal_condition, IsHungry)
        self.assertEqual(goal._goal_value, True)

    def test_multiple_objects(self):
        batman = Agent('batman')
        robin = Agent('robin')
        objects = [batman, robin]
        conditions = [IsHungry]
        goal = generate_goal(conditions, objects)
        self.assertIn(
            goal._goal_condition.planning_tuple,
            [
                (IsHungry, (batman,)),
                (IsHungry, (robin,))
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
        test_obj.is_hungry = False
        condition = IsHungry(test_obj)
        test_goal = Goal(
            "person is hungry", condition=condition, value=False)
        self.assertTrue(test_goal.is_satisfied())

    def test_not_satisfied(self):
        """Test a case where a goal is not satisfied."""
        test_obj = Agent("test agent")
        test_obj.is_hungry = True
        condition = IsHungry(test_obj)
        test_goal = Goal(
            "person is hungry", condition=condition, value=False)
        self.assertFalse(test_goal.is_satisfied())
