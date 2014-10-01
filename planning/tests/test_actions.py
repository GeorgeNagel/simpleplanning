import unittest

from planning.actions import Action
from planning.agents import Agent
from planning.conditions import Condition


# Test-related conditions
class HasSword(Condition):
    name = 'has sword'
    required_names = ['agent']

    def evaluate(self, **all_objects_dict):
        agent_key = self._object_names['agent']
        agent_obj = all_objects_dict[agent_key]
        if hasattr(agent_obj, 'has_sword'):
            return agent_obj.has_sword
        else:
            return False


class IsAlive(Condition):
    name = 'is alive'
    required_names = ['agent']

    def evaluate(self, **all_objects_dict):
        agent_key = self._object_names['agent']
        agent_obj = all_objects_dict[agent_key]
        if hasattr(agent_obj, 'is_hungry'):
            return agent_obj.is_hungry
        else:
            return True


# Test action
kill = Action(
    'kill',
    preconditions=[
        (IsAlive(agent='victim'), True)
    ],
    effects={
        (IsAlive(agent='victim'), False)
    }
)

suicide = Action(
    'suicide',
    preconditions={
        (IsAlive(agent='actor'), True)
    },
    effects={
        (IsAlive(agent='actor'), False)
    }
)


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

    def test_objects(self):
        self.assertEqual(kill.objects, ['victim'])

    def test_check_preconditions_failure(self):
        self.object.alive = False
        result = kill.check_preconditions(
            actor=self.actor, victim=self.object)
        self.assertFalse(result)

    def test_check_preconditions(self):
        result = kill.check_preconditions(
            actor=self.actor, victim=self.object)
        self.assertTrue(result)

    def test_agent_preconditions(self):
        result = suicide.check_preconditions(actor=self.actor)
        self.assertTrue(result)

    def test_check_preconditions_object_mismatch(self):
        """Test that a ValueError is raised for invalid objects."""
        self.assertRaises(
            ValueError,
            kill.check_preconditions,
            actor=self.actor,
            test="test"
        )

    def test_apply_action(self):
        """Test that applying an action has the desired effects."""
        kill.apply_action(actor=self.actor, victim=self.object)
        self.assertTrue(self.actor.alive)
        self.assertFalse(self.object.alive)

    def test_calculate_effects(self):
        effects = kill.calculate_effects(actor=self.actor, victim=self.object)
        self.assertEqual(
            effects,
            {(self.object, 'alive'): False}
        )

    def test_calculate_preconditions(self):
        preconditions = kill.calculate_preconditions(
            actor=self.actor, victim=self.object
        )
        self.assertEqual(
            preconditions,
            [(self.object, 'alive', True)]
        )
