from planning.actions import Action
from planning.agents import Agent
from planning.conditions import Condition, Is
from planning.goals import generate_goal
from planning.plans import select_plan


#Conditions
class HasSword(Condition):
    name = 'has sword'
    number_of_objects = 1

    def evaluate(self):
        eater_obj = self.objects[0]
        if hasattr(eater_obj, 'has_sword'):
            return eater_obj.has_sword
        else:
            return False


class IsAlive(Condition):
    name = 'is alive'
    number_of_objects = 1

    def evaluate(self):
        obj = self.objects[0]
        if hasattr(obj, 'alive'):
            return obj.alive
        else:
            return False


#Actions
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

    @classmethod
    def apply_action(self, actor=None, **objects):
        victim = objects['victim']
        victim.alive = False


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

    @classmethod
    def apply_action(self, actor=None, **objects):
        actor.has_sword = True
        victim = objects['victim']
        victim.has_sword = False


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

    @classmethod
    def apply_action(self, actor=None, **objects):
        actor.has_sword = False
        friend = objects['friend']
        friend.has_sword = True


arthur = Agent('Arthur')
arthur.has_sword = False
lancelot = Agent('Lancelot')
lancelot.has_sword = True
guinevere = Agent("Guinevere")
guinevere.has_sword = False

agents = [arthur, guinevere, lancelot]
available_actions = [Kill, StealSword, GiveSword]
conditions = [HasSword, IsAlive]

# Create goals for each agent
for agent in agents:
    agent._goal = generate_goal(conditions, agents)
    print "%s's goal: %s" % (agent._name, agent._goal)

MAX_TURNS = 20

game_over = False
number_of_turns = 0
while not game_over:
    number_of_turns += 1
    # Each agent takes a turn
    for agent in agents:
        print "%s's turn." % agent._name
        actions_sequence = select_plan(
            actor=agent, goal=agent._goal, available_actions=available_actions,
            objects=agents)
        if actions_sequence:
            next_action = actions_sequence[0]
        else:
            print "%s's goal is already satisfied." % agent._name
            game_over = True
            break
        actor, action, objects_dict = next_action
        # Perform the next action in the plan
        action.apply_action(actor=agent, **objects_dict)
        print "%s performs %s on %s" % (agent._name, action.name, objects_dict)
        
        # Check for game-ending conditions
        for agent in agents:
            if not agent.alive:
                print "%s is dead." % agent._name
                game_over = True
                break
        for agent in agents:
            if agent._goal.is_satisfied():
                print "%s's goal is satisfied." % agent._name
                game_over = True
                break
        if number_of_turns > MAX_TURNS:
            print "Game concluded with no winner."
            game_over = True
        if game_over:
            break
