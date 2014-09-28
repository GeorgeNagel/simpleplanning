from planning.actions import Action
from planning.agents import Agent
from planning.goals import generate_goal
from planning.plans import select_plan

arthur = Agent('Arthur')
arthur.has_sword = False
lancelot = Agent('Lancelot')
lancelot.has_sword = True
guinevere = Agent("Guinevere")
guinevere.has_sword = False

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
steal_sword = Action(
    "steal sword",
    preconditions={
        "victim__has_sword": True,
        "victim__is_not": 'actor',
        "actor__has_sword": False
    },
    effects={
        "victim__has_sword": False,
        "actor__has_sword": True,
    }
)
give_sword = Action(
    "give sword",
    preconditions={
        "friend__has_sword": False,
        "friend__is_not": 'actor',
        "actor__has_sword": True,
    },
    effects={
        "friend__has_sword": True,
        "actor__has_sword": False,
    }
)

agents = [arthur, guinevere, lancelot]
available_actions = [kill, steal_sword, give_sword]

# Create goals for each agent
for agent in agents:
    agent._goal = generate_goal(agents)
    print "%s's goal: %s" % (agent, agent._goal)

game_over = False
while not game_over:
    # Each agent takes a turn
    for agent in agents:
        print "%s's turn." % agent._name
        actions_sequence = select_plan(
            actor=agent, goal=agent._goal, available_actions=available_actions,
            objects=agents)
        next_action = actions_sequence[0]
        print "NEXT ACTION: %s" % repr(next_action)
        _, action, objects_dict = next_action
        # Perform the next action in the plan
        action.apply_action(actor=agent, **objects_dict)
        print "%s performs %s on %s" % (agent, action, objects_dict)
    if any(not agent.alive for agent in agents):
        game_over = True
