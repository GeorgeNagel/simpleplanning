import copy


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
        self._object_names = object_names
        if self.name is None:
            raise ValueError(
                "Must specify a name"
            )
        if not isinstance(object_names, list) and object_names is not None:
            raise ValueError(
                "object_names must be a list or None."
            )

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
        The tuple is in the form of (condition_instance, [obj_1, obj_2])
        """
        objects_list = self.objects_list_from_objects_dict(all_objects_dict)
        _planning_tuple = (self.__class__, objects_list)
        return _planning_tuple

    def objects_list_from_objects_dict(self, all_objects_dict):
        """Utility to return the list of objects for a condition."""
        objects_list = []
        for object_key in self._object_names:
            obj = all_objects_dict[object_key]
            objects_list.append(obj)
        return objects_list


class Is(Condition):
    name = 'is'

    def evaluate(self, **all_objects_dict):
        objects_list = self.objects_list_from_objects_dict(all_objects_dict)
        if objects_list[0] == objects_list[1]:
            return True
        else:
            raise ImpossibleException


class IsNot(Condition):
    name = 'is not'

    def evaluate(self, **all_objects_dict):
        objects_list = self.objects_list_from_objects_dict(all_objects_dict)
        if objects_list[0] != objects_list[1]:
            return True
        else:
            raise ImpossibleException
