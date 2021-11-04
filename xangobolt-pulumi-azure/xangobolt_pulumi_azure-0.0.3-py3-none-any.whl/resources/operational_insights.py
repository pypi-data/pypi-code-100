from pulumi.resource import ResourceOptions
import pulumi_azure_native.operationalinsights as operationalinsights
import pulumi
from pulumi_azure_native.operationalinsights import workspace

def Workspace(stem, props, resource_group, provider=None, parent=None, depends_on=None):
    ws = operationalinsights.Workspace(
        f'ws-{stem}',
        workspace_name=f'ws-{stem}',
        location=props.location,
        resource_group_name=resource_group,
        retention_in_days=90,
        sku=operationalinsights.WorkspaceSkuArgs(
            name="PerGB2018",
        ),
        tags=props.tags,
        opts=ResourceOptions(provider=provider, parent=parent, depends_on=depends_on)
    )
    return ws