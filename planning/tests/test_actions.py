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


class TestActions(unittest.TestCase):
    def setUp(self):
        # Create the test agents
        st_george = Agent('St. George')
        dragon = Agent('Dragon')

        # Add the test attributes
        st_george.alive = True
        dragon.alive = True
        self.agent = st_george
        self.object = dragon

    def test_check_preconditions_failure(self):
        self.object.alive = False
        result = check_preconditions(
            kill, self.agent, victim=self.object)
        self.assertFalse(result)

    def test_check_preconditions(self):
        result = check_preconditions(
            kill, self.agent, victim=self.object)
        self.assertTrue(result)

    def test_check_preconditions_object_mismatch(self):
        """Test that a ValueError is raised for invalid objects."""
        self.assertRaises(
            ValueError,
            check_preconditions,
            kill,
            self.agent,
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

        apply_action(kill, agent=st_george, victim=dragon)
        self.assertTrue(st_george.alive)
        self.assertFalse(dragon.alive)


class TestCalculateEffects(unittest.TestCase):
    def test_calculate_effects(self):
        test_agent = Agent('test_agent')
        test_obj = Agent('test_agent_2')
        effects = calculate_effects(kill, agent=test_agent, victim=test_obj)
        self.assertEqual(
            effects,
            {(test_obj, 'alive'): False}
        )
