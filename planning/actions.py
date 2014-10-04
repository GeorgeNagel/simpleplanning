from planning.settings import log


class Action(object):
    name = None
    preconditions = None
    effects = None

    def __init__(self):
        if any(
            [
                val is None for val in [
                    self.name, self.preconditions, self.effects
                ]
            ]
        ):
            raise ValueError("precondtions and effects must be specified.")

    def __repr__(self):
        return "<%s>" % self.name

    @classmethod
    def object_keys(cls):
        """A list of all objects involved in the action, excluding 'actor'."""
        objects = set()
        for precondition_tuple in cls.preconditions:
            precondition, condition_objects, value = precondition_tuple
            if isinstance(condition_objects, basestring):
                objects.add(condition_objects)
            else:
                objects.update(condition_objects)
        for effect_tuple in cls.effects:
            effect, condition_objects, value = effect_tuple
            if isinstance(condition_objects, basestring):
                objects.add(condition_objects)
            else:
                objects.update(condition_objects)
        if 'actor' in objects:
            objects.remove('actor')
        return list(objects)

    @classmethod
    def check_preconditions(cls, actor=None, **objects_dict):
        """Check to see if the preconditions for this action are met."""
        log.debug("Checking preconditions")
        log.debug("action: %s, actor: %s, objects: %s" % (
            cls.name, actor, objects_dict))

        all_objects = {'actor': actor}
        all_objects.update(objects_dict)

        # The object arguments must match those required by the preconditions
        if set(objects_dict.keys()) != set(cls.object_keys()):
            raise ValueError(
                "Input objects and action objects mismatch."
                " Input objects: %s. Output objects: %s." % (
                    set(objects_dict.keys()), set(cls.object_keys())
                )
            )

        # Check all the preconditions
        all_preconditions_met = True
        for precondition_tuple in cls.preconditions:
            condition_class, object_names, expected_value = precondition_tuple
            if isinstance(object_names, basestring):
                object_names = [object_names]
            objects_list = [all_objects[name] for name in object_names]
            condition_inst = condition_class(objects_list)
            actual_value = condition_inst.evaluate()
            if expected_value != actual_value:
                log.debug("MISMATCH: %s, expected: %s. actual: %s" % (
                    condition_class, expected_value, actual_value)
                )
                all_preconditions_met = False
                break
        log.debug("Preconditions met? %s" % all_preconditions_met)
        return all_preconditions_met

    @classmethod
    def apply_action(cls, actor=None, **objects):
        """Stub for subclasses to implement."""
        raise NotImplementedError

    @classmethod
    def calculate_effects(cls, actor=None, **objects):
        """Create an effects dict for planning activities."""
        all_objects_dict = {'actor': actor}
        all_objects_dict.update(objects)

        calculated_effects = {}
        for action_effect_tuple in cls.effects:
            condition_class, object_names, effect_value = action_effect_tuple
            if isinstance(object_names, basestring):
                object_names = [object_names]
            objects_list = [all_objects_dict[name] for name in object_names]
            condition_instance = condition_class(objects_list)
            # Get a tuple of the condition and its related objects
            planning_tuple = condition_instance.planning_tuple
            calculated_effects[planning_tuple] = effect_value
        return calculated_effects

    @classmethod
    def calculate_preconditions(cls, actor=None, **objects):
        """Create a list of preconditions tuples.
        These tuples represent the state prior to this action.

        Tuples are like (condition_class, object_tuple, value).
        """
        all_objects_dict = {'actor': actor}
        all_objects_dict.update(objects)

        calculated_preconditions = []
        for precondition_tuple in cls.preconditions:
            condition_class, object_names, value = precondition_tuple
            if isinstance(object_names, basestring):
                object_names = [object_names]
            # Create the list of objects by name
            objects_list = [all_objects_dict[name] for name in object_names]
            objects_tuple = tuple(objects_list)
            prior_state_tuple = (condition_class, objects_tuple, value)
            calculated_preconditions.append(prior_state_tuple)
        return calculated_preconditions
