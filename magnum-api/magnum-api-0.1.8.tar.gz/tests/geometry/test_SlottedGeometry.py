from magnumapi.cadata.CableDatabase import CableDatabase
from magnumapi.geometry.GeometryFactory import GeometryFactory
from tests.resource_files import create_resources_file_path


def test_init_slotted_geometry():
    # arrange
    json_path = create_resources_file_path('resources/geometry/roxie/16T/16T_abs_slotted.json')
    cadata_path = create_resources_file_path('resources/geometry/roxie/16T/roxieold_2.cadata')
    cadata = CableDatabase.read_cadata(cadata_path)

    # act
    geometry = GeometryFactory.init_slotted_with_json(json_path, cadata)

    # assert
    assert geometry.blocks[0].block_def.radius == 26.0
    assert geometry.blocks[4].block_def.radius == 40.35
    assert geometry.blocks[7].block_def.radius == 54.699999999999996
    assert geometry.blocks[10].block_def.radius == 69.5


def test_init_slotted_relative_geometry():
    # arrange
    json_path = create_resources_file_path('resources/geometry/roxie/16T/16T_rel_slotted.json')
    cadata_path = create_resources_file_path('resources/geometry/roxie/16T/roxieold_2.cadata')
    cadata = CableDatabase.read_cadata(cadata_path)

    # act
    geometry = GeometryFactory.init_slotted_with_json(json_path, cadata)

    # assert
    assert geometry.blocks[0].block_def.radius == 26.0
    assert geometry.blocks[4].block_def.radius == 40.35
    assert geometry.blocks[7].block_def.radius == 54.699999999999996
    assert geometry.blocks[10].block_def.radius == 69.5
