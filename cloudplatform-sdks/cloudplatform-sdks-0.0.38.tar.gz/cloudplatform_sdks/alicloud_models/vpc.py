from .clients import vpc_client


class AliVpc:

    """
    {
        "DescribeVpcsResponse": {
            "TotalCount": 2,
            "Vpcs": {
                "Vpc": {
                    "IsDefault": false,
                    "Status": "Available",
                    "CenStatus": "Attached",
                    "DhcpOptionsSetStatus": "Available",
                    "Description": "This is my VPC.",
                    "ResourceGroupId": "rg-acfmxazb4ph****",
                    "CidrBlock": "192.168.0.0/16",
                    "VRouterId": "vrt-bp1jcg5cmxjbl9xgc****",
                    "DhcpOptionsSetId": "dopt-o6w0df4epg9zo8isy****",
                    "OwnerId": 1234567,
                    "VpcId": "vpc-bp1qpo0kug3a20qqe****",
                    "CreationTime": "2018-04-18T15:02:37Z",
                    "VpcName": "vpc1",
                    "RegionId": "cn-hangzhou",
                    "Ipv6CidrBlock": "2408:XXXX:0:a600::/56",
                    "Ipv6CidrBlocks": {
                        "Ipv6CidrBlock": {
                            "Ipv6Isp": "BGP",
                            "Ipv6CidrBlock": "2408:XXXX:0:a600::/56"
                        }
                    },
                    "Tags": {
                        "Tag": {
                            "Value": "internal",
                            "Key": "env"
                        }
                    },
                    "VSwitchIds": {
                        "VSwitchId": "vsw-bp1nhbnpv2blyz8dl****"
                    },
                    "UserCidrs": {
                        "UserCidr": "10.0.0.0/8"
                    },
                    "NatGatewayIds": {
                        "NatGatewayIds": "nat-245xxxftwt45bg****"
                    },
                    "RouterTableIds": {
                        "RouterTableIds": "vtb-bp1krxxzp0c29fmon****"
                    },
                    "SecondaryCidrBlocks": {
                        "SecondaryCidrBlock": "192.168.20.0/24"
                    }
                }
            },
            "PageSize": 10,
            "RequestId": "C6532AA8-D0F7-497F-A8EE-094126D441F5",
            "PageNumber": 1
        }
    }
    ;;vpc attribute
        {
        "DescribeVpcAttributeResponse": {
            "IsDefault": false,
            "Status": "Available",
            "DhcpOptionsSetStatus": "Available",
            "Description": "VPC",
            "ResourceGroupId": "rg-acfmxazbvgb4ph****",
            "ClassicLinkEnabled": false,
            "RequestId": "7486AE4A-129D-43DB-A714-2432C074BA04",
            "VSwitchIds": {
                "VSwitchId": "{\"VSwitchId\": [ \"vsw-bp14cagpfysr29feg****\" ]}"
            },
            "SecondaryCidrBlocks": {
                "SecondaryCidrBlock": "192.168.0.0/16"
            },
            "CidrBlock": "192.168.0.0/16",
            "UserCidrs": {
                "UserCidr": "172.16.0.1/24"
            },
            "VRouterId": "vrt-bp1jso6ng1at0ajsc****",
            "DhcpOptionsSetId": "dopt-o6w0df4epg9zo8isy****",
            "OwnerId": 12345678,
            "VpcId": "vpc-bp18sth14qii3pnvo****",
            "AssociatedCens": {
                "AssociatedCen": {
                    "CenStatus": "Attached",
                    "CenOwnerId": 111111111111,
                    "CenId": "cen-7qthudw0ll6jmc****"
                }
            },
            "CreationTime": "2020-10-16T07:31:09Z",
            "VpcName": "doctest2",
            "RegionId": "cn-hangzhou",
            "Ipv6CidrBlock": "2408:XXXX:0:a600::/56",
            "Ipv6CidrBlocks": {
                "Ipv6CidrBlock": {
                    "Ipv6Isp": "BGP",
                    "Ipv6CidrBlock": "2408:XXXX:0:6a::/56"
                }
            },
            "CloudResources": {
                "CloudResourceSetType": {
                    "ResourceCount": 1,
                    "ResourceType": "VSwitch"
                }
            }
        }
    }
    ;;; VSwitches
    {
        "PageNumber": 1,
        "VSwitches": {
            "VSwitch": [
                {
                    "RouteTable": {
                        "RouteTableId": "vtb-hp3hk68xybfogay8g****",
                        "RouteTableType": "System"
                    },
                    "Description": "",
                    "IsDefault": false,
                    "AvailableIpAddressCount": 252,
                    "ResourceGroupId": "rg-acfmxazb4ph****",
                    "ZoneId": "cn-huhehaote-a",
                    "VSwitchId": "vsw-hp3l11aj1tx5g8qwt****",
                    "NetworkAclId": "",
                    "VpcId": "vpc-hp37qeafxj2sfs69s****",
                    "CreationTime": "2019-11-11T03:39:17Z",
                    "Status": "Available",
                    "CidrBlock": "192.168.0.0/24",
                    "Ipv6CidrBlock": "2408:4004:0:a600::/64",
                    "VSwitchName": "CL-IPv6-VSW"
                }
            ]
        },
        "TotalCount": 1,
        "PageSize": 10,
        "RequestId": "95C297E1-E9F7-4EB8-BE42-82C8CEBF994D"
    }
    ;;; vswitch attributes
        {
        "RouteTable":{
            "RouteTableId":"vtb-hp3ngu1hkdutfakqn****",
            "RouteTableType":"System"
        },
        "Description":"",
        "IsDefault":false,
        "AvailableIpAddressCount":251,
        "ResourceGroupId":"rg-acfmy45w7w2****",
        "ZoneId":"cn-huhehaote-a",
        "VSwitchId":"vsw-hp3lyltb1dosj540y****",
        "VpcId":"vpc-hp34hflqqsjh3a3q7****",
        "CreationTime":"2019-01-07T04:54:14Z",
        "Status":"Available",
        "CidrBlock":"192.168.0.0/24",
        "RequestId":"A31F062D-81F0-48BC-9771-915D6622D26A",
        "Ipv6CidrBlock":"2408:4004:0:2900::/64",
        "VSwitchName":"doc1",
        "CloudResources":{
            "CloudResourceSetType":[]
        }
    }
    ;;; eip describe
        {
        "TotalCount": 10,
        "PageSize": 10,
        "RequestId": "4EC47282-1B74-4534-BD0E-403F3EE64CAF",
        "EipAddresses": {
            "EipAddress": {
                "HDMonitorStatus": false,
                "ServiceManaged": 0,
                "ResourceGroupId": "rg-acfmxazcdxs****",
                "AllocationId": "eip-2zeerraiwb7ujcdvf****",
                "SecondLimited": false,
                "BusinessStatus": "Normal",
                "Name": "test",
                "SegmentInstanceId": "eipsg-t4nr90yik5oy38xd****",
                "ReservationOrderType": "RENEWCHANGE",
                "InstanceRegionId": "cn-hangzhou",
                "ExpiredTime": "2019-04-29T02:00Z",
                "Bandwidth": 5,
                "BandwidthPackageId": "cbwp-bp1ego3i4j07ccdvf****",
                "ReservationActiveTime": "2019-03-11T16:00:00Z",
                "InstanceType": "EcsInstance",
                "ReservationBandwidth": 12,
                "Status": "Associating",
                "InstanceId": "i-bp15zckdt37cdvf****",
                "ISP": "BGP",
                "HasReservationData": false,
                "DeletionProtection": true,
                "BandwidthPackageType": "CommonBandwidthPackage",
                "BandwidthPackageBandwidth": 50,
                "ReservationInternetChargeType": "PayByBandwidth",
                "InternetChargeType": "PayByBandwidth",
                "AllocationTime": "2019-04-23T01:37:38Z",
                "Descritpion": "abc",
                "EipBandwidth": 101,
                "Netmode": "public",
                "ChargeType": "PostPaid",
                "IpAddress": "116.XX.XX.28",
                "RegionId": "cn-hangzhou",
                "OperationLocks": {
                    "LockReason": {
                        "LockReason": "financial"
                    }
                },
                "AvailableRegions": {
                    "AvailableRegion": "cn-hangzhou"
                }
            }
        },
        "PageNumber": 10
    }
    """
    STATUS_MAPPER = {
        'Available': 'available',
        'InUse': 'inuse',
        'Deleted': 'deleted',
        'Pending': 'pending',
    }

    def __init__(self, vpc_info):
        self.vpc_info = vpc_info

    @classmethod
    def get_vpc_list(cls, params=None):
        res = vpc_client.describe_vpcs(params)
        if 'DescribeVpcsResponse' in res:
            return res
        return []

    @classmethod
    def get_vpc_attribute(cls, params=None):
        res = vpc_client.describe_vpcs(params)
        if 'DescribeVpcAttributeResponse' in res:
            return res
        return []

    @classmethod
    def get_vswitches_list(cls, params=None):
        res = vpc_client.describe_vswitches(params)
        if 'VSwitches' in res:
            return res
        return []

    @classmethod
    def get_vswitches_attribute(cls, params=None):
        res = vpc_client.describe_vswitch_attributes(params)
        if 'VSwitchId' in res:
            return res
        return []

    @classmethod
    def get_eip_address(cls, params=None):
        res = vpc_client.describe_eip_address(params)
        if 'EipAddresses' in res:
            return res
        return []