from .clients import ess_client


class AliEss:
    """
    {
     "TotalCount": 1,
     "PageSize": 10,
     "RequestId": "D66AC79E-8299-4E0B-B681-3063C88E215B",
     "PageNumber": 1,
     "ScalingInstances": {
      "ScalingInstance": [
       {
        "LoadBalancerWeight": 50,
        "CreatedTime": "2020-12-21T03:11:00Z",
        "WarmupState": "NoNeedWarmup",
        "ZoneId": "cn-hangzhou-g",
        "InstanceId": "i-m5e3z5l951fibnd9****",
        "ScalingActivityId": "asa-bp1c9djwrgxjyk31****",
        "ScalingGroupId": "asg-m5e8n5qw4atki7f6****",
        "HealthStatus": "Healthy",
        "CreationTime": "2020-12-21T03:11Z",
        "LifecycleState": "InService",
        "Entrusted": true,
        "ScalingConfigurationId": "asc-m5e9vcoen45jspz7****",
        "CreationType": "AutoCreated"
       }
      ]
     },
     "TotalSpotCount": 0
    }
    """
    def __init__(self, ess_info=None):
        self.ess_info = ess_info

    @classmethod
    def get_list(cls, params=None):
        res = ess_client.describe_scaling_instances(params)
        if 'ScalingInstances' in res:
            return res
        return []

    @classmethod
    def get_scaling_groups(cls, params=None):
        res = ess_client.describe_scaling_groups(params)
        if 'ScalingGroups' in res:
            return res
        return []