class Agent(object):
    def __init__(self, name):
        self._name = name
        self.alive = True

    def __repr__(self):
        return "<%s>" % self._name
