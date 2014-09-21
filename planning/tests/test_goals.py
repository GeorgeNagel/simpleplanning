import unittest

from planning.goals import generate_goal


class Agent(object):
    def __init__(self, name):
        self.name = name
    alive = True


class TestStuff(unittest.TestCase):
    def test_generate_goal(self):
        batman = Agent('batman')
        objects = [batman]
        goal = generate_goal(objects)
        self.assertEqual(
            goal,
            (batman, 'alive', False)
        )

    def test_multiple_objects(self):
        batman = Agent('batman')
        robin = Agent('robin')
        robin.alive = False
        objects = [batman, robin]
        goal = generate_goal(objects)
        self.assertIn(
            goal,
            [
                (batman, 'alive', False),
                (robin, 'alive', True)
            ]
        )
