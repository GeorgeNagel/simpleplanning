import unittest

from planning.actions import Action
from planning.agents import Agent


# Test action
kill = Action(
    'kill',
    preconditions={
        'victim__alive': True,
    },
    effects={
        'victim__alive': False,
    }
)

suicide = Action(
    'suicide',
    preconditions={
        'actor__alive': True,
    },
    effects={
        'actor__alive': False,
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
