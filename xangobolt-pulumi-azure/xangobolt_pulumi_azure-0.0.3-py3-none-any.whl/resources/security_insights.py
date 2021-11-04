from pulumi.resource import ResourceOptions
import pulumi_azure_native.securityinsights as securityInsights
import pulumi
from pulumi_azure_native.securityinsights.data_connector import DataConnectorArgs
from resources import operational_insights

def Sentinel(stem, props, resource_group, workspace=None, provider=None, parent=None, depends_on=None):
    sentinel = securityInsights.SentinelOnboardingState(
        f'stnl-{stem}',
        sentinel_onboarding_state_name="default",
        customer_managed_key=False,
        operational_insights_resource_provider="Microsoft.OperationalInsights",
        resource_group_name=resource_group,
        workspace_name=workspace or operational_insights.Workspace(stem, props=props, resource_group=resource_group, provider=provider, parent=parent),
        opts=ResourceOptions(provider=provider, parent=parent, depends_on=depends_on)
    )
    return sentinel

def Ueba(stem, props, resource_group, workspace, provider=None, parent=None, depends_on=None):
    ueba = securityInsights.Ueba("Ueba",
        operational_insights_resource_provider="Microsoft.OperationalInsights",
        resource_group_name=resource_group,
        settings_name="Ueba",
        kind="Ueba",
        data_sources=["AuditLogs", "AzureActivity", "SecurityEvent", "SigninLogs"],
        workspace_name=workspace,
        opts=ResourceOptions(provider=provider, parent=parent, depends_on=depends_on)
    )
    return ueba

def EntityAnalytics(stem, props, resource_group, workspace, provider=None, parent=None, depends_on=None):
    ea = securityInsights.EntityAnalytics("EntityAnalytics",
        operational_insights_resource_provider="Microsoft.OperationalInsights",
        resource_group_name=resource_group,
        settings_name="EntityAnalytics",
        kind="EntityAnalytics",
        workspace_name=workspace,
        opts=ResourceOptions(provider=provider, parent=parent, depends_on=depends_on)
    )
    return ea


def ASCConnector(stem, props, resource_group, workspace, subscription, provider=None, parent=None, depends_on=None):
    ascc = securityInsights.ASCDataConnector("ascDataConnector",
        kind="AzureSecurityCenter",
        resource_group_name=resource_group,
        workspace_name=workspace,
        data_types=securityInsights.AlertsDataTypeOfDataConnectorArgs(alerts={"state": "enabled"}),
        subscription_id=subscription,
        opts=ResourceOptions(provider=provider, parent=parent, depends_on=depends_on)
    )
    return ascc

def AADDataConnector(stem, props, resource_group, workspace, tenant_id, provider=None, parent=None, depends_on=None):
    aaddc = securityInsights.AADDataConnector("aadDataConnector",
        kind="AzureActiveDirectory",
        resource_group_name=resource_group,
        workspace_name=workspace,
        data_types=securityInsights.AlertsDataTypeOfDataConnectorArgs(alerts={"state": "enabled"}),
        tenant_id=tenant_id,
        opts=ResourceOptions(provider=provider, parent=parent, depends_on=depends_on)
    )
    return aaddc
    