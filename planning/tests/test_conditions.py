import unittest

from planning.actions import Action
from planning.agents import Agent
from planning.conditions import (
    Condition, Is, IsNot, ImpossibleException)


class IsHungry(Condition):
    name = 'is hungry'
    number_of_objects = 1

    def evaluate(self):
        eater_obj = self.objects[0]
        if hasattr(eater_obj, 'is_hungry'):
            return eater_obj.is_hungry
        else:
            return False

class HasSword(Condition):
    name = 'is hungry'
    number_of_objects = 1

    def evaluate(self):
        eater_obj = self.objects[0]
        if hasattr(eater_obj, 'has_sword'):
            return eater_obj.has_sword
        else:
            return False

class TestCondition(unittest.TestCase):
    """Test the Condition class."""
    def test_evaluate_not_implemented(self):
        """The evaluate() method must be implemented."""
        class IsFoolish(Condition):
            name = 'is foolish'
            number_of_objects = 0

        # Instantiate the condition object
        is_foolish = IsFoolish()
        self.assertRaises(
            NotImplementedError,
            is_foolish.evaluate,
        )

    def test_planning_tuple(self):
        test_agent = Agent('test agent')
        agent_is_hungry = IsHungry([test_agent])
        planning_tup = agent_is_hungry.planning_tuple
        self.assertEqual(
            planning_tup,
            (IsHungry, (test_agent,))
        )


class TestIsHungryCondition(unittest.TestCase):
    def test_is_hungry(self):
        knight = Agent('Knight')
        knight_is_hungry = IsHungry(knight)
        result = knight_is_hungry.evaluate()
        self.assertFalse(result)

    def test_is_not_hungry(self):
        knight = Agent('Knight')
        knight.is_hungry = True
        knight_is_hungry = IsHungry(knight)
        result = knight_is_hungry.evaluate()
        self.assertTrue(result)


class TestIsCondition(unittest.TestCase):
    def test_equivalent(self):
        agent = Agent("test agent")
        one_is_one = Is([agent, agent])
        result = one_is_one.evaluate()
        self.assertTrue(result)

    def test_not_equivalent(self):
        """Evaluation should raise ImpossibleException."""
        agent_1 = Agent("first agent")
        agent_2 = Agent("second agent")
        one_is_two = Is([agent_1, agent_2])
        self.assertRaises(
            ImpossibleException,
            one_is_two.evaluate
        )


class TestIsNotCondition(unittest.TestCase):
    def test_not_equivalent(self):
        agent_1 = Agent("first agent")
        agent_2 = Agent("second agent")
        one_is_not_two = IsNot([agent_1, agent_2])
        result = one_is_not_two.evaluate()
        self.assertTrue(result)

    def test_equivalent(self):
        """Evaluation should raise ImpossibleException."""
        agent = Agent("test agent")
        one_is_not_one = IsNot([agent, agent])
        self.assertRaises(
            ImpossibleException,
            one_is_not_one.evaluate
        )
