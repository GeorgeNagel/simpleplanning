import unittest

from planning.actions import (
    apply_action, check_preconditions, calculate_effects)
from planning.agent import Agent


# Test action
kill = {
    'objects': ['victim'],
    'preconditions': {
        'victim__alive': True,
    },
    'effects': {
        'victim__alive': False,
    }
}

suicide = {
    'objects': [],
    'preconditions': {
        'actor__alive': True,
    },
    'effects': {
        'actor__alive': False,
    }
}


class TestActions(unittest.TestCase):
    def setUp(self):
        # Create the test agents
        st_george = Agent('St. George')
        dragon = Agent('Dragon')

        # Add the test attributes
        st_george.alive = True
        dragon.alive = True
        self.actor = st_george
        self.object = dragon

    def test_check_preconditions_failure(self):
        self.object.alive = False
        result = check_preconditions(
            kill, actor=self.actor, victim=self.object)
        self.assertFalse(result)

    def test_check_preconditions(self):
        result = check_preconditions(
            kill, actor=self.actor, victim=self.object)
        self.assertTrue(result)

    def test_agent_preconditions(self):
        result = check_preconditions(
            suicide, actor=self.actor)
        self.assertTrue(result)

    def test_check_preconditions_object_mismatch(self):
        """Test that a ValueError is raised for invalid objects."""
        self.assertRaises(
            ValueError,
            check_preconditions,
            kill,
            actor=self.actor,
            test="test"
        )

    def test_apply_action(self):
        """Test that applying an action has the desired effects."""
        # Create the test agents
        st_george = Agent('St. George')
        dragon = Agent('Dragon')

        # Add the test attributes
        st_george.alive = True
        dragon.alive = True

        apply_action(kill, actor=st_george, victim=dragon)
        self.assertTrue(st_george.alive)
        self.assertFalse(dragon.alive)


class TestCalculateEffects(unittest.TestCase):
    def test_calculate_effects(self):
        test_actor = Agent('test_agent')
        test_obj = Agent('test_agent_2')
        effects = calculate_effects(kill, actor=test_actor, victim=test_obj)
        self.assertEqual(
            effects,
            {(test_obj, 'alive'): False}
        )
