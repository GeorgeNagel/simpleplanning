import unittest

from planning.agents import Agent
from planning.conditions import (
    Condition, HasSword, Is, IsNot, ImpossibleException)


class IsHungry(Condition):
    name = 'is hungry'
    required_names = ['eater']

    def evaluate(self, **all_objects_dict):
        eater_key = self._object_names['eater']
        eater_obj = all_objects_dict[eater_key]
        if hasattr(eater_obj, 'is_hungry'):
            return eater_obj.is_hungry
        else:
            return False


class TestCondition(unittest.TestCase):
    """Test the Condition class."""
    def test_evaluate_not_implemented(self):
        """The evaluate() method must be implemented."""
        class IsFoolish(Condition):
            name = 'is foolish'
            required_names = []

        # Instantiate the condition object
        is_foolish = IsFoolish()
        self.assertRaises(
            NotImplementedError,
            is_foolish.evaluate,
        )

    def test_object_names(self):
        is_hungry = IsHungry(eater='actor')
        object_names = is_hungry.object_names
        self.assertEqual(object_names, ['eater'])

class TestHasSword(unittest.TestCase):
    def test_no_sword(self):
        knight = Agent('Knight')
        has_sword = HasSword(agent='knight')
        result = has_sword.evaluate(knight=knight)
        self.assertFalse(result)

    def test_has_sword(self):
        knight = Agent('Knight')
        knight.has_sword = True
        has_sword = HasSword(agent='knight')
        result = has_sword.evaluate(knight=knight)
        self.assertTrue(result)

class TestIsCondition(unittest.TestCase):
    def test_equivalent(self):
        agent = Agent("test agent")
        _is = Is(obj_1='agent_1', obj_2='agent_2')
        result = _is.evaluate(agent_1=agent, agent_2=agent)
        self.assertTrue(result)

    def test_not_equivalent(self):
        """Evaluation should raise ImpossibleException."""
        agent_1 = Agent("first agent")
        agent_2 = Agent("second agent")
        _is = Is(obj_1='agent_1', obj_2='agent_2')
        self.assertRaises(
            ImpossibleException,
            _is.evaluate,
            agent_1=agent_1,
            agent_2=agent_2
        )


class TestIsNotCondition(unittest.TestCase):
    def test_not_equivalent(self):
        agent_1 = Agent("first agent")
        agent_2 = Agent("second agent")
        _is_not = IsNot(obj_1='agent_1', obj_2='agent_2')
        result = _is_not.evaluate(agent_1=agent_1, agent_2=agent_2)
        self.assertTrue(result)

    def test_equivalent(self):
        """Evaluation should raise ImpossibleException."""
        agent = Agent("test agent")
        _is_not = IsNot(obj_1='agent_1', obj_2='agent_2')
        self.assertRaises(
            ImpossibleException,
            _is_not.evaluate,
            agent_1=agent,
            agent_2=agent
        )

