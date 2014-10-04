import unittest

from planning.actions import Action
from planning.conditions import Condition, Is
from planning.goals import Goal
from planning.plans import (
    PossiblePlan, select_plan, breadth_first_plan_search,
    _create_initial_plan, _actions_that_match_possible_plan,
    _action_effects_match_possible_plan, PlanningDepthException)


class Agent(object):
    def __init__(self, name):
        self._name = name
    alive = True
    has_sword = False

    def __repr__(self):
        """Helpful method for using repr() when debugging."""
        return '<' + self._name + ' ' + str(id(self)) + '>'


# Test-related conditions
class HasSword(Condition):
    name = 'is hungry'
    number_of_objects = 1

    def evaluate(self):
        eater_obj = self.objects[0]
        if hasattr(eater_obj, 'has_sword'):
            return eater_obj.has_sword
        else:
            return False


class IsAlive(Condition):
    name = 'is hungry'
    number_of_objects = 1

    def evaluate(self):
        obj = self.objects[0]
        if hasattr(obj, 'alive'):
            return obj.alive
        else:
            return False


# Test actions
class GetSword(Action):
    name = 'get sword',
    number_of_objects = 0
    preconditions = [
        (HasSword, 'actor', False)
    ]
    effects = [
        (HasSword, 'actor', True)
    ]


class Kill(Action):
    name = "kill"
    number_of_objects = 1
    preconditions = [
        (IsAlive, 'victim', True),
        (HasSword, 'actor', True)
    ]
    effects = [
        (IsAlive, 'victim', False)
    ]


class StealSword(Action):
    name = 'steal sword'
    number_of_objects = 1
    preconditions = [
        (HasSword, 'victim', True),
        (HasSword, 'actor', False),
        (Is, ('victim', 'actor'), False)
    ]
    effects = [
        (HasSword, 'victim', False),
        (HasSword, 'actor', True)
    ]


class GiveSword(Action):
    name = 'give sword'
    number_of_objects = 1
    preconditions = [
        (HasSword, 'friend', False),
        (HasSword, 'actor', True),
        (Is, ('friend', 'actor'), False)
    ]
    effects = [
        (HasSword, 'friend', True),
        (HasSword, 'actor', False)
    ]


class TestPlanning(unittest.TestCase):
    def setUp(self):
        self.knight = Agent('Knight')
        self.dragon = Agent('Dragon')
        self.possible_actions = [Kill, GetSword]
        dragon_is_alive = IsAlive(self.dragon)
        self.knight_goal = Goal(
            'dragon dead', condition=dragon_is_alive, value=False)
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
                (self.knight, GetSword, {}),
                (self.knight, Kill, {'victim': self.dragon}),
            ]
        )

    def test_three_actions(self):
        arthur = Agent("Arthur")
        arthur.has_sword = False
        lancelot = Agent("Lancelot")
        lancelot.has_sword = True
        guenivere = Agent("Guenivere")
        guenivere.has_sword = False

        available_actions = [Kill, StealSword, GiveSword]
        objects = [arthur, lancelot, guenivere]

        guenivere_is_alive = IsAlive(guenivere)
        arthur_goal = Goal(
            'guenivere dead',
            condition=guenivere_is_alive,
            value=False
        )
        actions_sequence = select_plan(
            actor=arthur, goal=arthur_goal,
            available_actions=available_actions,
            objects=objects)
        self.assertEqual(
            actions_sequence,
            [
                (arthur, StealSword, {'victim': lancelot}),
                (arthur, Kill, {'victim': guenivere})
            ]
        )


class TestBreadthFirstPlanSearch(unittest.TestCase):
    def setUp(self):
        self.knight = Agent('Knight')
        self.dragon = Agent('Dragon')
        self.possible_actions = [Kill, GetSword]
        dragon_is_alive = IsAlive(self.dragon)
        self.knight_goal = Goal(
            'dragon dead', condition=dragon_is_alive, value=False)
        self.objects = [self.knight, self.dragon]

    def test_goal_already_met(self):
        """Test that a plan is returned when it matches initial conditions."""
        possible_plan = PossiblePlan()
        possible_plan.conditions = {(IsAlive, (self.dragon,)): True}
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
            [(self.knight, Kill, {'victim': self.dragon})]
        )

    def test_no_inputs(self):
        """Ensure that a ValueError is raised for no inputs."""
        self.assertRaises(ValueError, breadth_first_plan_search)

    def test_depth_exception(self):
        self.knight.has_sword = False
        available_actions = [Kill]
        self.assertRaises(
            PlanningDepthException,
            breadth_first_plan_search,
            actor=self.knight,
            goal=self.knight_goal,
            available_actions=available_actions,
            objects=self.objects
        )


class TestPossiblePlan(unittest.TestCase):
    """Test the PossiblePlan object."""
    def setUp(self):
        self.knight = Agent('Knight')
        self.dragon = Agent('Dragon')
        self.possible_actions = [Kill, GetSword]
        dragon_is_alive = IsAlive(self.dragon)
        self.knight_goal = Goal(
            'dragon dead', condition=dragon_is_alive, value=False)
        self.objects = [self.knight, self.dragon]

    def test_create_initial_plan(self):
        """Test that initial conditions are created correctly."""

        initial_plan = _create_initial_plan(self.knight_goal)
        self.assertEqual(
            initial_plan.conditions,
            {(IsAlive, (self.dragon,)): False}
        )

    def test_possible_plan_matches_initial(self):
        """Check that a possible plan matches initial conditions."""
        possible_plan = PossiblePlan()
        possible_plan.conditions = {
            (IsAlive, (self.knight,)): True,
            (HasSword, (self.knight,)): False,
            (IsAlive, (self.dragon,)): True
        }
        matches = possible_plan.matches_initial_conditions()
        self.assertTrue(matches)

    def test_copy(self):
        possible_plan = PossiblePlan()
        possible_plan.conditions = {
            (IsAlive, (self.knight,)): True,
        }
        possible_plan.actions_to_perform = [
            (self.knight, Kill, {'victim': self.dragon})
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
            (HasSword, (self.knight,)): True,
            (IsAlive, (self.dragon,)): True
        }
        possible_plan.actions_to_perform = [
            (self.knight, Kill, {'victim': self.dragon})
        ]
        # Prepend the GetSword action
        possible_plan.prepend_action(
            (self.knight, GetSword, {})
        )
        self.assertEqual(
            possible_plan.conditions,
            {
                (HasSword, (self.knight,)): False,
                (IsAlive, (self.dragon,)): True
            }
        )
        self.assertEqual(
            possible_plan.actions_to_perform,
            [
                (self.knight, GetSword, {}),
                (self.knight, Kill, {'victim': self.dragon})
            ]
        )

    def test_prepend_action_multiple(self):
        """Test that multiple actions cause conditions to update properly."""
        arthur = Agent("Arthur")
        arthur.has_sword = False
        lancelot = Agent("Lancelot")
        lancelot.has_sword = True
        guenivere = Agent("Guenivere")
        guenivere.has_sword = False
        possible_plan = PossiblePlan()
        possible_plan.prepend_action(
            (arthur, Kill, {'victim': guenivere})
        )
        possible_plan.prepend_action(
            (arthur, StealSword, {'victim': lancelot})
        )
        self.assertEqual(
            possible_plan.conditions,
            {
                (Is, (lancelot, arthur)): False,
                (HasSword, (lancelot,)): True,
                (HasSword, (arthur,)): False,
                (IsAlive, (guenivere,)): True
            }
        )


class TestActionsThatMatchPossiblePlan(unittest.TestCase):
    def setUp(self):
        self.actions = [Kill, GetSword]
        self.knight = Agent('knight')
        self.dragon = Agent('dragon')

    def test_actions_that_match_possible_plan(self):
        possible_plan = PossiblePlan()
        possible_plan.conditions = {
            (IsAlive, (self.dragon,)): False
        }
        actions = _actions_that_match_possible_plan(
            possible_plan, available_actions=self.actions,
            actor=self.knight, objects=[self.knight, self.dragon])
        self.assertEqual(
            actions,
            [(self.knight, Kill, {'victim': self.dragon})]
        )

    def test_action_effects_match_possible_plan(self):
        possible_plan = PossiblePlan()
        possible_plan.conditions = {
            (IsAlive, (self.dragon,)): False
        }
        matches = _action_effects_match_possible_plan(
            Kill, possible_plan=possible_plan, actor=self.knight,
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
            Kill, possible_plan=possible_plan, actor=self.knight,
            victim=self.knight
        )
        self.assertFalse(matches)
