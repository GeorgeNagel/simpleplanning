import sys

from planning.agent import Agent
from planning.goals import generate_goal

arthur = Agent('Arthur')
arthur.has_sword = False
lancelot = Agent('Lancelot')
lancelot.has_sword = True
guinevere = Agent("Guinevere")
guinevere.has_sword = False


agents = [arthur, guinevere, lancelot]

# Create goals for each agent
for agent in agents:
    agent._goal = generate_goal(agents)