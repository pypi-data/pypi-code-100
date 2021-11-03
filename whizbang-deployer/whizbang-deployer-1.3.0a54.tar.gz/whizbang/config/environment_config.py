from typing import List, Optional

from pydantic import BaseModel

from whizbang.domain.models.keyvault.keyvault_access_policy import KeyVaultAccessPolicy
from whizbang.domain.models.rbac_policy import RBACPolicy


class EnvironmentConfig(BaseModel):
    subscription_id: str = None
    tenant_id: str = None
    resource_group_name: str = None
    resource_group_location: str = None
    resource_name_prefix: str = None
    resource_name_suffix: str = None
    environment: str = None

    # todo: remove
    vnet_address_prefix: str = None

    # nested
    rbac_policies: Optional[List[RBACPolicy]] = []
    keyvault_access_policies: Optional[List[KeyVaultAccessPolicy]] = []
