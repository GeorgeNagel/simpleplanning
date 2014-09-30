class ImpossibleException(Exception):
    pass


class Condition(object):
    # Name of the condition
    name = None
    # A dict mapping condition names to action names
    _object_names = None
    # A list of names of objects consumed by this condition
    required_names = None

    def __init__(self, **object_names):
        """Condition constructor.

        PARAMETERS
        * name - The name of the condition.
        * **object_names - A dict like {'wizard': 'actor'}
        """
        self._object_names = object_names
        if not isinstance(self.required_names, list):
            raise ValueError("required_names must be a list.")
        # Ensure that all the required names are used
        used_names = set()
        for name in object_names.keys():
            used_names.add(name)
        if used_names != set(self.required_names):
            raise ValueError(
                "All of the following must be defined: %s" %
                set(self.required_names)
            )
        if self.name is None:
            raise ValueError(
                "Must specify a name"
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


class HasSword(Condition):
    name='has sword'
    required_names=['agent']

    def evaluate(self, **all_objects_dict):
        agent_key = self._object_names['agent']
        agent_obj = all_objects_dict[agent_key]
        if hasattr(agent_obj, 'has_sword'):
            return agent_obj.has_sword
        else:
            return False


class Is(Condition):
    name='is'
    required_names=['obj_1', 'obj_2']

    def evaluate(self, **all_objects_dict):
        obj_1_key = self._object_names['obj_1']
        obj_2_key = self._object_names['obj_2']
        obj_1 = all_objects_dict[obj_1_key]
        obj_2 = all_objects_dict[obj_2_key]
        if obj_1 == obj_2:
            return True
        else:
            raise ImpossibleException


class IsNot(Condition):
    name='is not'
    required_names=['obj_1', 'obj_2']

    def evaluate(self, **all_objects_dict):
        obj_1_key = self._object_names['obj_1']
        obj_2_key = self._object_names['obj_2']
        obj_1 = all_objects_dict[obj_1_key]
        obj_2 = all_objects_dict[obj_2_key]
        if obj_1 != obj_2:
            return True
        else:
            raise ImpossibleException
