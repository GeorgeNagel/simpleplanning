import unittest

from planning.actions import Action
from planning.goals import Goal
from planning.plans import (
    PossiblePlan, select_plan, breadth_first_plan_search,
    _create_initial_plan, _actions_that_match_possible_plan,
    _action_effects_match_possible_plan)


class Agent(object):
    def __init__(self, name):
        self._name = name
    alive = True
    has_sword = False

    def __repr__(self):
        """Helpful method for using repr() when debugging."""
        return (
            '<' + self._name + '. has_sword: %s. alive: %s.>' % (
                self.has_sword, self.alive
            )
        )

# Test actions
get_sword = Action(
    'get sword',
    preconditions={
        "actor__has_sword": False,
    },
    effects={
        "actor__has_sword": True,
    }
)

kill = Action(
    "kill",
    preconditions={
        "victim__alive": True,
        "actor__has_sword": True,
    },
    effects={
        "victim__alive": False,
    }
)


class TestPlanning(unittest.TestCase):
    def setUp(self):
        self.knight = Agent('Knight')
        self.dragon = Agent('Dragon')
        self.possible_actions = [kill, get_sword]
        self.knight_goal = Goal(
            'dragon dead', obj=self.dragon, attr_name='alive', value=False)
        self.objects = [self.knight, self.dragon]

    def test_planning(self):
        actions_sequence = select_plan(
            actor=self.knight, goal=self.knight_goal,
            available_actions=self.possible_actions,
            objects=self.objects
        )
        self.assertEqual(
            actions_sequence,
            [
                (self.knight, get_sword, {}),
                (self.knight, kill, {'victim': self.dragon}),
            ]
        )


class TestBreadthFirstPlanSearch(unittest.TestCase):
    def setUp(self):
        self.knight = Agent('Knight')
        self.dragon = Agent('Dragon')
        self.possible_actions = [kill, get_sword]
        self.knight_goal = Goal(
            'dragon dead', obj=self.dragon, attr_name='alive', value=False)
        self.objects = [self.knight, self.dragon]

    def test_goal_already_met(self):
        """Test that a plan is returned when it matches initial conditions."""
        possible_plan = PossiblePlan()
        possible_plan.conditions = {(self.dragon, 'alive'): True}
        selected_plan = breadth_first_plan_search(
            actor=self.knight, goal=self.knight_goal,
            available_actions=self.possible_actions,
            objects=self.objects, possible_plans=[possible_plan]
        )
        self.assertEqual(selected_plan, possible_plan)

    def test_breadth_first_plan_search(self):
        """Test the breadth-first plan search algorithm."""
        # Shortcut so that there is only one action needed
        self.knight.has_sword = True
        selected_history = breadth_first_plan_search(
            actor=self.knight, goal=self.knight_goal,
            available_actions=self.possible_actions,
            objects=self.objects, possible_plans=[])
        self.assertEqual(
            selected_history.actions_to_perform,
            [(self.knight, kill, {'victim': self.dragon})]
        )

    def test_no_inputs(self):
        """Ensure that a ValueError is raised for no inputs."""
        self.assertRaises(ValueError, breadth_first_plan_search)


class TestPossiblePlan(unittest.TestCase):
    """Test the PossiblePlan object."""
    def setUp(self):
        self.knight = Agent('Knight')
        self.dragon = Agent('Dragon')
        self.possible_actions = [kill, get_sword]
        self.knight_goal = Goal(
            'dragon dead', obj=self.dragon, attr_name='alive', value=False)
        self.objects = [self.knight, self.dragon]

    def test_create_initial_plan(self):
        """Test that initial conditions are created correctly."""

        initial_plan = _create_initial_plan(self.knight_goal)
        self.assertEqual(
            initial_plan.conditions,
            {(self.dragon, 'alive'): False}
        )

    def test_possible_plan_matches_initial(self):
        """Check that a possible plan matches initial conditions."""
        possible_plan = PossiblePlan()
        possible_plan.conditions = {
            (self.knight, 'alive'): True,
            (self.knight, 'has_sword'): False,
            (self.dragon, 'alive'): True
        }
        matches = possible_plan.matches_initial_conditions()
        self.assertTrue(matches)

    def test_copy(self):
        possible_plan = PossiblePlan()
        possible_plan.conditions = {
            (self.knight, 'alive'): True,
        }
        possible_plan.actions_to_perform = [
            (self.knight, kill, {'victim': self.dragon})
        ]
        copy_possible_plan = possible_plan.copy()

        # The internal properties should be the same, but
        # they should not be the same location in memory
        self.assertEqual(
            possible_plan.conditions,
            copy_possible_plan.conditions
        )
        self.assertEqual(
            possible_plan.actions_to_perform,
            copy_possible_plan.actions_to_perform
        )
        self.assertFalse(
            possible_plan.conditions is copy_possible_plan.conditions
        )
        self.assertFalse(
            possible_plan.actions_to_perform is
            copy_possible_plan.actions_to_perform
        )
        self.assertFalse(possible_plan is copy_possible_plan)

    def test_prepend_action(self):
        # Create the plan
        possible_plan = PossiblePlan()
        possible_plan.conditions = {
            (self.knight, 'has_sword'): True,
            (self.dragon, 'alive'): True,
        }
        possible_plan.actions_to_perform = [
            (self.knight, kill, {'victim': self.dragon})
        ]
        # Prepend the get_sword action
        possible_plan.prepend_action(
            (self.knight, get_sword, {})
        )
        self.assertEqual(
            possible_plan.conditions,
            {
                (self.knight, 'has_sword'): False,
                (self.dragon, 'alive'): True,
            }
        )
        self.assertEqual(
            possible_plan.actions_to_perform,
            [
                (self.knight, get_sword, {}),
                (self.knight, kill, {'victim': self.dragon})
            ]
        )


class TestActionsThatMatchPossiblePlan(unittest.TestCase):
    def setUp(self):
        self.actions = [kill, get_sword]
        self.knight = Agent('knight')
        self.dragon = Agent('dragon')

    def test_actions_that_match_possible_plan(self):
        possible_plan = PossiblePlan()
        possible_plan.conditions = {
            (self.dragon, 'alive'): False
        }
        actions = _actions_that_match_possible_plan(
            possible_plan, available_actions=self.actions,
            actor=self.knight, objects=[self.knight, self.dragon])
        self.assertEqual(
            actions,
            [(self.knight, kill, {'victim': self.dragon})]
        )

    def test_action_effects_match_possible_plan(self):
        possible_plan = PossiblePlan()
        possible_plan.conditions = {
            (self.dragon, 'alive'): False
        }
        matches = _action_effects_match_possible_plan(
            kill, possible_plan=possible_plan, actor=self.knight,
            victim=self.dragon
        )
        self.assertTrue(matches)

    def test_action_effects_no_match(self):
        """Test a case when the action effects do not match plan conditions."""
        possible_plan = PossiblePlan()
        possible_plan.conditions = {
            (self.dragon, 'alive'): False
        }
        matches = _action_effects_match_possible_plan(
            kill, possible_plan=possible_plan, actor=self.knight,
            victim=self.knight
        )
        self.assertFalse(matches)
