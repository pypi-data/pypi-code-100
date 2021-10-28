"""This module contains the general information for BiosVfOperationMode ManagedObject."""

from ...imcmo import ManagedObject
from ...imccoremeta import MoPropertyMeta, MoMeta
from ...imcmeta import VersionMeta


class BiosVfOperationModeConsts:
    VP_OPERATION_MODE_TEST_ONLY = "Test Only"
    VP_OPERATION_MODE_TEST_AND_REPAIR = "Test and Repair"
    VP_OPERATION_MODE_PLATFORM_DEFAULT = "platform-default"


class BiosVfOperationMode(ManagedObject):
    """This is BiosVfOperationMode class."""

    consts = BiosVfOperationModeConsts()
    naming_props = set([])

    mo_meta = {
        "classic": MoMeta("BiosVfOperationMode", "biosVfOperationMode", "Operation-Mode", VersionMeta.Version421a, "InputOutput", 0x1f, [], ["admin"], ['biosPlatformDefaults', 'biosSettings'], [], [None]),
    }


    prop_meta = {

        "classic": {
            "child_action": MoPropertyMeta("child_action", "childAction", "string", VersionMeta.Version421a, MoPropertyMeta.INTERNAL, None, None, None, None, [], []),
            "dn": MoPropertyMeta("dn", "dn", "string", VersionMeta.Version421a, MoPropertyMeta.READ_WRITE, 0x2, 0, 255, None, [], []),
            "rn": MoPropertyMeta("rn", "rn", "string", VersionMeta.Version421a, MoPropertyMeta.READ_WRITE, 0x4, 0, 255, None, [], []),
            "status": MoPropertyMeta("status", "status", "string", VersionMeta.Version421a, MoPropertyMeta.READ_WRITE, 0x8, None, None, None, ["", "created", "deleted", "modified", "removed"], []),
            "vp_operation_mode": MoPropertyMeta("vp_operation_mode", "vpOperationMode", "string", VersionMeta.Version421a, MoPropertyMeta.READ_WRITE, 0x10, None, None, None, ["Test Only", "Test and Repair", "platform-default"], []),
        },

    }

    prop_map = {

        "classic": {
            "childAction": "child_action", 
            "dn": "dn", 
            "rn": "rn", 
            "status": "status", 
            "vpOperationMode": "vp_operation_mode", 
        },

    }

    def __init__(self, parent_mo_or_dn, **kwargs):
        self._dirty_mask = 0
        self.child_action = None
        self.status = None
        self.vp_operation_mode = None

        ManagedObject.__init__(self, "BiosVfOperationMode", parent_mo_or_dn, **kwargs)

