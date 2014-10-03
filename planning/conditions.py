class ImpossibleException(Exception):
    pass


class Condition(object):
    # Name of the condition
    name = None
    # A list of the names to be used for the condition
    _object_names = None

    def __init__(self, object_names=None):
        """Condition constructor.

        PARAMETERS
        * name - The name of the condition.
        * object_names - A list like ['actor', 'victim']
        """
        if self.name is None:
            raise ValueError(
                "Must specify a name"
            )
        if not isinstance(object_names, (list, basestring)) \
                and object_names is not None:
            raise ValueError(
                "object_names must be a list or None."
            )
        if isinstance(object_names, basestring):
            # Handle the special case where object_names is a single name
            object_names = [object_names]

        self._object_names = object_names

    @property
    def object_names(self):
        """Return the names of all objects involved in the condition."""
        # Note: Excludes 'actor'
        objects = set()
        for obj_name in self._object_names:
            if obj_name != "actor":
                objects.add(obj_name)
        return list(objects)

    def evaluate(self, **all_objects_dict):
        """Evaluate the truth value of this condition.

        PARAMETERS:
        * all_objects_dict - A dict of all objects being evaluated"""
        # Raise ImpossibleException if the condition evaluated on these objects
        # will never return True, regardless of any actions evaluated prior.
        raise NotImplementedError

    def planning_tuple(self, **all_objects_dict):
        """Return the tuple to be used for planning.
        This tuple will be a key in the conditions dictionary,
        and is in the form of (condition_class, (obj_1, obj_2))
        """
        objects_tuple = self.objects_tuple(**all_objects_dict)
        _planning_tuple = (self.__class__, objects_tuple)
        return _planning_tuple

    def objects_tuple(self, **all_objects_dict):
        """Utility to return a tuple of all of the objects for a condition."""
        objects_list = []
        for object_key in self._object_names:
            obj = all_objects_dict[object_key]
            objects_list.append(obj)
        return tuple(objects_list)


class Is(Condition):
    name = 'is'

    def evaluate(self, **all_objects_dict):
        objects_tuple = self.objects_tuple(**all_objects_dict)
        if objects_tuple[0] == objects_tuple[1]:
            return True
        else:
            raise ImpossibleException


class IsNot(Condition):
    name = 'is not'

    def evaluate(self, **all_objects_dict):
        objects_tuple = self.objects_tuple(**all_objects_dict)
        if objects_tuple[0] != objects_tuple[1]:
            return True
        else:
            raise ImpossibleException
