import unittest

from planning.actions import Action
from planning.agents import Agent
from planning.conditions import Condition


# Test-related conditions
class HasSword(Condition):
    name = 'is hungry'

    def evaluate(self, **all_objects_dict):
        objects_list = self.objects_tuple(**all_objects_dict)
        eater_obj = objects_list[0]
        if hasattr(eater_obj, 'has_sword'):
            return eater_obj.has_sword
        else:
            return False


class IsAlive(Condition):
    name = 'is hungry'

    def evaluate(self, **all_objects_dict):
        objects_list = self.objects_tuple(**all_objects_dict)
        eater_obj = objects_list[0]
        if hasattr(eater_obj, 'is_alive'):
            return eater_obj.is_alive
        else:
            return False


# Test actions
class Kill(Action):
    name = "kill"
    preconditions = [
        (IsAlive('victim'), True)
    ]
    effects = [
        (IsAlive('victim'), False)
    ]

    @classmethod
    def apply_action(cls, actor=None, **objects):
        victim = objects['victim']
        victim.is_alive = False


class Suicide(Action):
    name = 'suicide',
    preconditions = [
        (IsAlive('actor'), True)
    ]
    effects = [
        (IsAlive('actor'), False)
    ]

    @classmethod
    def apply_action(cls, actor=None, **objects):
        actor.is_alive = False


class TestActions(unittest.TestCase):
    """Test the Action class."""
    def setUp(self):
        # Create the test agents
        st_george = Agent('St. George')
        dragon = Agent('Dragon')

        # Add the test attributes
        st_george.alive = True
        dragon.alive = True
        self.actor = st_george
        self.object = dragon

    def test_object_keys(self):
        self.assertEqual(Kill.object_keys(), ['victim'])

    def test_check_preconditions_failure(self):
        self.object.alive = False
        result = Kill.check_preconditions(
            actor=self.actor, victim=self.object)
        self.assertFalse(result)

    def test_check_preconditions(self):
        result = Kill.check_preconditions(
            actor=self.actor, victim=self.object)
        self.assertTrue(result)

    def test_agent_preconditions(self):
        result = Suicide.check_preconditions(actor=self.actor)
        self.assertTrue(result)

    def test_check_preconditions_object_mismatch(self):
        """Test that a ValueError is raised for invalid objects."""
        self.assertRaises(
            ValueError,
            Kill.check_preconditions,
            actor=self.actor,
            test="test"
        )

    def test_apply_action(self):
        """Test that applying an action has the desired effects."""
        Kill.apply_action(actor=self.actor, victim=self.object)
        self.assertTrue(self.actor.alive)
        self.assertFalse(self.object.alive)

    def test_calculate_effects(self):
        effects = Kill.calculate_effects(actor=self.actor, victim=self.object)
        self.assertEqual(
            effects,
            {(IsAlive, (self.object,)): False}
        )

    def test_calculate_preconditions(self):
        preconditions = Kill.calculate_preconditions(
            actor=self.actor, victim=self.object
        )
        self.assertEqual(
            preconditions,
            [(IsAlive, (self.object,), True)]
        )
