"""This module contains the general information for BiosVfNvmdimmPerformConfig ManagedObject."""

from ...imcmo import ManagedObject
from ...imccoremeta import MoPropertyMeta, MoMeta
from ...imcmeta import VersionMeta


class BiosVfNvmdimmPerformConfigConsts:
    VP_NVMDIMM_PERFORM_CONFIG_BW_OPTIMIZED = "BW Optimized"
    VP_NVMDIMM_PERFORM_CONFIG_BALANCED_PROFILE = "Balanced Profile"
    VP_NVMDIMM_PERFORM_CONFIG_LATENCY_OPTIMIZED = "Latency Optimized"
    VP_NVMDIMM_PERFORM_CONFIG_PLATFORM_DEFAULT = "platform-default"


class BiosVfNvmdimmPerformConfig(ManagedObject):
    """This is BiosVfNvmdimmPerformConfig class."""

    consts = BiosVfNvmdimmPerformConfigConsts()
    naming_props = set([])

    mo_meta = {
        "classic": MoMeta("BiosVfNvmdimmPerformConfig", "biosVfNvmdimmPerformConfig", "NVM-Performance-Setting", VersionMeta.Version412a, "InputOutput", 0x1f, [], ["admin"], ['biosPlatformDefaults', 'biosSettings'], [], [None]),
        "modular": MoMeta("BiosVfNvmdimmPerformConfig", "biosVfNvmdimmPerformConfig", "NVM-Performance-Setting", VersionMeta.Version412a, "InputOutput", 0x1f, [], ["admin"], ['biosPlatformDefaults', 'biosSettings'], [], [None])
    }


    prop_meta = {

        "classic": {
            "dn": MoPropertyMeta("dn", "dn", "string", VersionMeta.Version412a, MoPropertyMeta.READ_WRITE, 0x2, 0, 255, None, [], []),
            "rn": MoPropertyMeta("rn", "rn", "string", VersionMeta.Version412a, MoPropertyMeta.READ_WRITE, 0x4, 0, 255, None, [], []),
            "status": MoPropertyMeta("status", "status", "string", VersionMeta.Version412a, MoPropertyMeta.READ_WRITE, 0x8, None, None, None, ["", "created", "deleted", "modified", "removed"], []),
            "vp_nvmdimm_perform_config": MoPropertyMeta("vp_nvmdimm_perform_config", "vpNvmdimmPerformConfig", "string", VersionMeta.Version412a, MoPropertyMeta.READ_WRITE, 0x10, None, None, None, ["BW Optimized", "Balanced Profile", "Latency Optimized", "platform-default"], []),
            "child_action": MoPropertyMeta("child_action", "childAction", "string", VersionMeta.Version412a, MoPropertyMeta.INTERNAL, None, None, None, None, [], []),
        },

        "modular": {
            "dn": MoPropertyMeta("dn", "dn", "string", VersionMeta.Version412a, MoPropertyMeta.READ_WRITE, 0x2, 0, 255, None, [], []),
            "rn": MoPropertyMeta("rn", "rn", "string", VersionMeta.Version412a, MoPropertyMeta.READ_WRITE, 0x4, 0, 255, None, [], []),
            "status": MoPropertyMeta("status", "status", "string", VersionMeta.Version412a, MoPropertyMeta.READ_WRITE, 0x8, None, None, None, ["", "created", "deleted", "modified", "removed"], []),
            "vp_nvmdimm_perform_config": MoPropertyMeta("vp_nvmdimm_perform_config", "vpNvmdimmPerformConfig", "string", VersionMeta.Version412a, MoPropertyMeta.READ_WRITE, 0x10, None, None, None, ["BW Optimized", "Balanced Profile", "Latency Optimized", "platform-default"], []),
            "child_action": MoPropertyMeta("child_action", "childAction", "string", VersionMeta.Version412a, MoPropertyMeta.INTERNAL, None, None, None, None, [], []),
        },

    }

    prop_map = {

        "classic": {
            "dn": "dn", 
            "rn": "rn", 
            "status": "status", 
            "vpNvmdimmPerformConfig": "vp_nvmdimm_perform_config", 
            "childAction": "child_action", 
        },

        "modular": {
            "dn": "dn", 
            "rn": "rn", 
            "status": "status", 
            "vpNvmdimmPerformConfig": "vp_nvmdimm_perform_config", 
            "childAction": "child_action", 
        },

    }

    def __init__(self, parent_mo_or_dn, **kwargs):
        self._dirty_mask = 0
        self.status = None
        self.vp_nvmdimm_perform_config = None
        self.child_action = None

        ManagedObject.__init__(self, "BiosVfNvmdimmPerformConfig", parent_mo_or_dn, **kwargs)

