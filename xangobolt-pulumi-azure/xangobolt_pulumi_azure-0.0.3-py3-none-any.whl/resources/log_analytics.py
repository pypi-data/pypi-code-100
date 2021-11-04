from arpeggio.cleanpeg import NOT, prefix
from pulumi.resource import ResourceOptions
import pulumi_azure_native.operationalinsights as ops_insights

def workspace(stem, props, resource_group, provider=None, parent=None, depends_on=None):
    kv = ops_insights.Workspace(
        f'kv-{stem}',
        vault_name=f'kv-{stem}',
        resource_group_name= resource_group,
        tags=props.tags,
        location=props.location,
        properties=keyvault.VaultPropertiesArgs(
            sku=keyvault.SkuArgs(
                family="A",
                name="standard"
            ),
            tenant_id=props.tenantId,
            ),
        opts=ResourceOptions(provider=provider, parent=parent, depends_on=depends_on)
    )
    return kv

