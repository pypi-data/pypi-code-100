from pulumi import ComponentResource, ResourceOptions, StackReference
from resources import operational_insights, security_insights, resource_group


class AzureSentinel(ComponentResource):
    def __init__(self, name: str, props: None, opts: ResourceOptions = None):
        super().__init__('Sentinel', name, {}, opts)

        Resources = [security_insights, operational_insights]

        for resource in Resources:
            resource.location = props.location
            # resource.resource_group_name = props.resource_group_name
            resource.self = self
            resource.tags = props.tags

        sentinel_rg = resource_group.resource_group(
            name, 
            props=props,
            provider=opts.providers.get('xangobolt')
        )

        sentinel_workspace = operational_insights.Workspace(
            name,
            props,
            resource_group=sentinel_rg.name,
            provider=opts.providers.get('xangobolt')
        )

        xb_sentinel = security_insights.Sentinel(
            name, 
            props=props,
            resource_group=sentinel_rg.name,
            workspace=sentinel_workspace.name,
            provider=opts.providers.get('xangobolt')
        )

        ascc = security_insights.ASCConnector(
            name,
            props=props,
            resource_group=sentinel_rg.name,
            workspace=sentinel_workspace.name,
            subscription="7d1c32f6-e23e-438d-898d-33cc978366cf",
            provider=opts.providers.get('xangobolt')
        )

        # aaddc = security_insights.AADDataConnector(
        #     name,
        #     props=props,
        #     resource_group=sentinel_rg.name,
        #     workspace=sentinel_workspace.name,
        #     tenant_id="31b0748d-e5fe-4629-8f5e-66c5191556c9",
        #     provider=opts.providers.get('xangobolt')
        # )

        ea = security_insights.EntityAnalytics(
            name,
            props=props,
            resource_group=sentinel_rg.name,
            workspace=sentinel_workspace.name,
            provider=opts.providers.get('xangobolt')
        )

        ueba = security_insights.Ueba(
            name,
            props=props,
            resource_group=sentinel_rg.name,
            workspace=sentinel_workspace.name,
            provider=opts.providers.get('xangobolt')
        )