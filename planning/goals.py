import random

from planning.settings import log


def generate_goal(objects):
    """
    Returns an object, attribute, value pair.
    Assumes that all attributes can be modified by actions.
    Assumes all attributes are boolean.
    """
    log.debug("Generating goal.")
    possible_tuples = []
    for obj in objects:
        public_props = (name for name in dir(obj) if not name.startswith('_'))
        for public_prop in public_props:
            value = getattr(obj, public_prop)
            possible_tuples.append((obj, public_prop, not value))
    # Select a random one.
    selected_goal_tuple = random.choice(possible_tuples)
    return selected_goal_tuple
