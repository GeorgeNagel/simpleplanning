class ImpossibleException(Exception):
    pass


class Condition(object):
    # Name of the condition
    name = None
    objects = None
    number_of_objects = -1

    def __init__(self, objects=None):
        """Condition constructor.

        PARAMETERS
        * objects - A list of objects on which the condition will be evaluated.
        """
        if self.name is None:
            raise ValueError("Must specify a name")

        # Maintain objects as a list despite whatever was given to us
        if objects is None:
            objects = []
        elif not isinstance(objects, list):
            objects = [objects]

        if self.number_of_objects < 0:
            raise ValueError("number_of_objects must be zero or greater.")

        if len(objects) != self.number_of_objects:
            raise ValueError("Must use %d objects, got %d objects." % (
                self.number_of_objects, len(objects))
            )

        self.objects = objects


    def evaluate(self):
        """Evaluate the truth value of this condition."""
        # Raise ImpossibleException if the condition evaluated on these objects
        # will never return True, regardless of any actions evaluated prior.
        raise NotImplementedError

    @property
    def planning_tuple(self):
        """Return the tuple to be used for planning.
        This tuple will be a key in the conditions dictionary,
        and is in the form of (condition_class, (obj_1, obj_2))
        """
        objects_tuple = tuple(self.objects)
        _planning_tuple = (self.__class__, objects_tuple)
        return _planning_tuple


class Is(Condition):
    name = 'is'
    number_of_objects = 2

    def evaluate(self):
        if self.objects[0] == self.objects[1]:
            return True
        else:
            raise ImpossibleException


class IsNot(Condition):
    name = 'is not'
    number_of_objects = 2

    def evaluate(self):
        if self.objects[0] != self.objects[1]:
            return True
        else:
            raise ImpossibleException
