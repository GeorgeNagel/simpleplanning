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
        for precondition in self.preconditions:
            obj_name, attr_name = precondition.split('__')
            objects.add(obj_name)
        for effect in self.effects:
            obj_name, attr_name = effect.split('__')
            objects.add(obj_name)
        if 'actor' in objects:
            objects.remove('actor')
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
        for precondition in self.preconditions:
            # Split the precondition into the object and its attribute
            obj_name, attr_name = precondition.split("__")
            obj = all_objects[obj_name]
            precondition_value = self.preconditions[precondition]
            actual_value = getattr(obj, attr_name)

            if precondition_value != actual_value:
                all_preconditions_met = False
                break
        log.debug("Preconditions met? %s" % all_preconditions_met)
        return all_preconditions_met


    def apply_action(self, actor=None, **objects):
        if not self.check_preconditions(actor=actor, **objects):
            raise ValueError(
                "Preconditions not passed."
            )

        # Dict of all objects (including the actor)
        all_objects = {'actor': actor}
        all_objects.update(objects)

        for effect in self.effects:
            # Split the effect into the object and its attribute
            obj_name, attr_name = effect.split("__")
            obj = all_objects[obj_name]
            effect_value = self.effects[effect]
            setattr(obj, attr_name, effect_value)


    def calculate_effects(self, actor=None, **objects):
        """Calculate the effects tuple for planning activities."""
        calculated_effects = {}
        for action_effect in self.effects:
            # Parse the effect condition/value pair
            obj_name, attr_name = action_effect.split('__')
            effect_value =self.effects[action_effect]

            # Find the actual object by name in the objects dict
            # Include the actor in the list of objects
            objects.update({'actor': actor})
            obj = objects[obj_name]

            calculated_effects[(obj, attr_name)] = effect_value
        return calculated_effects


    def calculate_preconditions(self, actor=None, **objects):
        """Create the list of preconditions tuples like (obj, attr_name, value)."""
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
