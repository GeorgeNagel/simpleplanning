import unittest

from planning.agents import Agent
from planning.conditions import (
    Condition, Is, IsNot, ImpossibleException)


class IsHungry(Condition):
    name = 'is hungry'

    def evaluate(self, **all_objects_dict):
        objects_list = self.objects_list_from_objects_dict(all_objects_dict)
        eater_obj = objects_list[0]
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
        is_hungry = IsHungry(['hungry_guy'])
        object_names = is_hungry.object_names
        self.assertEqual(object_names, ['hungry_guy'])

    def test_planning_tuple(self):
        is_hungry = IsHungry(['hungry_guy'])
        test_agent = Agent('test agent')
        planning_tup = is_hungry.planning_tuple(
            hungry_guy=test_agent, maroon=5)
        self.assertEqual(
            planning_tup,
            (IsHungry, [test_agent])
        )

    def test_objects_list_from_objects_dict(self):
        is_hungry = IsHungry(['hungry_guy'])
        test_agent = Agent('hungry agent')
        objects_list = is_hungry.objects_list_from_objects_dict(
            {'hungry_guy': test_agent}
        )
        self.assertEqual(objects_list, [test_agent])


class TestIsHungryCondition(unittest.TestCase):
    def test_is_hungry(self):
        knight = Agent('Knight')
        is_hungry_condition = IsHungry(['knight'])
        result = is_hungry_condition.evaluate(knight=knight)
        self.assertFalse(result)

    def test_is_not_hungry(self):
        knight = Agent('Knight')
        knight.is_hungry = True
        is_hungry_condition = IsHungry(['knight'])
        result = is_hungry_condition.evaluate(knight=knight)
        self.assertTrue(result)


class TestIsCondition(unittest.TestCase):
    def test_equivalent(self):
        agent = Agent("test agent")
        _is = Is(['agent_1', 'agent_2'])
        result = _is.evaluate(agent_1=agent, agent_2=agent)
        self.assertTrue(result)

    def test_not_equivalent(self):
        """Evaluation should raise ImpossibleException."""
        agent_1 = Agent("first agent")
        agent_2 = Agent("second agent")
        _is = Is(['agent_1', 'agent_2'])
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
        _is_not = IsNot(['agent_1', 'agent_2'])
        result = _is_not.evaluate(agent_1=agent_1, agent_2=agent_2)
        self.assertTrue(result)

    def test_equivalent(self):
        """Evaluation should raise ImpossibleException."""
        agent = Agent("test agent")
        _is_not = IsNot(['agent_1', 'agent_2'])
        self.assertRaises(
            ImpossibleException,
            _is_not.evaluate,
            agent_1=agent,
            agent_2=agent
        )
