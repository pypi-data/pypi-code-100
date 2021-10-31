from .interaction import Interaction
from .system import System


def _wrap_system(system):
    from atooms.trajectory.decorators import change_species
    new_system = System()
    new_system.update(system)
    new_system = change_species(new_system, 'F')
    return new_system


def _add_interaction(trajectory, system):
    """
    Add interaction to trajectory from model metadata information or
    accompanying json file.
    """
    try:
        import atooms.models
    except ImportError:
        return system

    try:
        # Lookup in atooms models database
        # TODO: accept serialized json potential/cutoff in metadata
        name = trajectory.metadata['model']
        db = atooms.models.load()
        model = db[name]
    except KeyError:
        # If that fails, look for an accompanying json file
        try:
            model = atooms.models.read_json(trajectory.filename + '.json')
        except IOError:
            return system

    system.interaction = Interaction(model,
                                     interaction='interaction.f90',
                                     helpers='helpers_3d.f90',
                                     inline=True)
    return system


# Boost all trajectory classes with specific jit callbacks
# and create a new Trajectory factory that only loads these classes
# They keep their original names but live in this module namespace
# The original classes are untouched.
from atooms.trajectory import Trajectory as __Trajectory
from atooms.trajectory.factory import TrajectoryFactory
import copy

Trajectory = copy.deepcopy(__Trajectory)
Trajectory.register_callback(_wrap_system)

# Trajectory = TrajectoryFactory()
# for key in __Trajectory.formats:
#     new_name = __Trajectory.formats[key].__name__
#     old_cls = __Trajectory.formats[key]
#     cls = type(new_name, (old_cls, ), dict(old_cls.__dict__))
#     cls.add_class_callback(_wrap_system)
#     cls.add_self_callback(_add_interaction)
#     Trajectory.add(cls)

# # Lock the xyz format
# Trajectory.suffixes['xyz'] = Trajectory.formats['xyz']
