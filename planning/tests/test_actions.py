import unittest

from planning.actions import apply_action, check_preconditions
from planning.agent import Agent


class TestActions(unittest.TestCase):
    def setUp(self):
        self.action = {
            'objects': ['victim'],
            'preconditions': {
                'victim__alive': True,
            },
            'effects': {
                'victim__alive': False,
            }
        }
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
            self.action, self.agent, victim=self.object)
        self.assertFalse(result)

    def test_check_preconditions(self):
        result = check_preconditions(
            self.action, self.agent, victim=self.object)
        self.assertTrue(result)

    def test_check_preconditions_object_mismatch(self):
        """Test that a ValueError is raised for invalid objects."""
        self.assertRaises(
            ValueError,
            check_preconditions,
            self.action,
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

        apply_action(self.action, agent=st_george, victim=dragon)
        self.assertTrue(st_george.alive)
        self.assertFalse(dragon.alive)
