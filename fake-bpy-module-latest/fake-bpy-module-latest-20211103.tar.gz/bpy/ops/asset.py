import sys
import typing


def assign_action():
    ''' Set this pose Action as active Action on the active Object :file: addons/pose_library/operators.py\:213 <https://developer.blender.org/diffusion/BA/addons/pose_library/operators.py$213> _

    '''

    pass


def catalog_delete(catalog_id: str = ""):
    ''' Remove an asset catalog from the asset library (contained assets will not be affected and show up as unassigned)

    :param catalog_id: Catalog ID, ID of the catalog to delete
    :type catalog_id: str
    '''

    pass


def catalog_new(parent_path: str = ""):
    ''' Create a new catalog to put assets in

    :param parent_path: Parent Path, Optional path defining the location to put the new catalog under
    :type parent_path: str
    '''

    pass


def catalog_redo():
    ''' Redo the last undone edit to the asset catalogs

    '''

    pass


def catalog_undo():
    ''' Undo the last edit to the asset catalogs

    '''

    pass


def catalog_undo_push():
    ''' Store the current state of the asset catalogs in the undo buffer

    '''

    pass


def catalogs_save():
    ''' Make any edits to any catalogs permanent by writing the current set up to the asset library

    '''

    pass


def clear(set_fake_user: bool = False):
    ''' Delete all asset metadata and turn the selected asset data-blocks back into normal data-blocks

    :param set_fake_user: Set Fake User, Ensure the data-block is saved, even when it is no longer marked as asset
    :type set_fake_user: bool
    '''

    pass


def list_refresh():
    ''' Trigger a reread of the assets

    '''

    pass


def mark():
    ''' Enable easier reuse of selected data-blocks through the Asset Browser, with the help of customizable metadata (like previews, descriptions and tags)

    '''

    pass


def open_containing_blend_file():
    ''' Open the blend file that contains the active asset :file: startup/bl_operators/assets.py\:111 <https://developer.blender.org/diffusion/B/browse/master/release/scripts/startup/bl_operators/assets.py$111> _

    '''

    pass


def tag_add():
    ''' Add a new keyword tag to the active asset :file: startup/bl_operators/assets.py\:52 <https://developer.blender.org/diffusion/B/browse/master/release/scripts/startup/bl_operators/assets.py$52> _

    '''

    pass


def tag_remove():
    ''' Remove an existing keyword tag from the active asset :file: startup/bl_operators/assets.py\:75 <https://developer.blender.org/diffusion/B/browse/master/release/scripts/startup/bl_operators/assets.py$75> _

    '''

    pass
