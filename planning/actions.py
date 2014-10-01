from planning.settings import log


class Action(object):
    name = ''
    preconditions = None
    effects = None

    def __init__(self, name, preconditions=None, effects=None):
        if any([kw is None for kw in [preconditions, effects]]):
            raise ValueError("precondtions and effects must be specified.")
        self.name = name
        self.preconditions = preconditions
        self.effects = effects

    def __repr__(self):
        return "<%s>" % self.name

    @property
    def objects(self):
        """A list of all objects involved in the action, excluding 'actor'."""
        objects = set()
        for precondition_tuple in self.preconditions:
            precondition, value = precondition_tuple
            condition_object_names = precondition.object_names
            objects.update(condition_object_names)
        for effect_tuple in self.effects:
            effect, value = effect_tuple
            effect_object_names = effect.object_names
            objects.update(effect_object_names)
        return list(objects)

    def check_preconditions(self, actor=None, **objects_dict):
        """Check to see if the preconditions for this action are met."""
        log.debug("Checking preconditions")
        log.debug("action: %s, actor: %s, objects: %s" % (
            self.name, actor, objects_dict))

        all_objects = {'actor': actor}
        all_objects.update(objects_dict)

        # The object arguments must match those required by the preconditions
        if set(objects_dict.keys()) != set(self.objects):
            raise ValueError(
                "Input objects and action objects mismatch."
                " Input objects: %s. Output objects: %s." % (
                    set(objects_dict.keys()), set(self.objects)
                )
            )

        # Check all the preconditions
        all_preconditions_met = True
        for precondition_tuple in self.preconditions:
            precondition, expected_value = precondition_tuple
            actual_value = precondition.evaluate(**all_objects)
            if expected_value != actual_value:
                all_preconditions_met = False
                break
        log.debug("Preconditions met? %s" % all_preconditions_met)
        return all_preconditions_met

    def apply_action(self, actor=None, **objects):
        """Stub for subclasses to implement."""
        raise NotImplementedError

    def calculate_effects(self, actor=None, **objects):
        """Calculate the effects tuple for planning activities."""
        all_objects_dict = {'actor': actor}
        all_objects_dict.update(objects)

        calculated_effects = {}
        for action_effect_tuple in self.effects:
            action_effect_condition, effect_value = action_effect_tuple
            # Get a tuple of the condition and its related objects
            planning_tuple = action_effect_condition.planning_tuple(
                **all_objects_dict
            )
            calculated_effects[planning_tuple] = effect_value
        return calculated_effects

    def calculate_preconditions(self, actor=None, **objects):
        """Create a list of preconditions tuples.

        Tuples are like (obj, attr_name, value).
        """
        all_objects = {'actor': actor}
        all_objects.update(objects)

        preconditions_tuples = []
        for precondition in self.preconditions:
            # Split the precondition into the object and its attribute
            obj_name, attr_name = precondition.split("__")
            obj = all_objects[obj_name]
            precondition_value = self.preconditions[precondition]
            preconditions_tuple = (obj, attr_name, precondition_value)
            preconditions_tuples.append(preconditions_tuple)
        return preconditions_tuples
