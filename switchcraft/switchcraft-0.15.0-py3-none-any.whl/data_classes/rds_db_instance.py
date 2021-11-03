"""RDS DB Instance.

Data Class representing a RDS DB Instance. This is a common object returned by
the 'DescribeDBInstances' API.
"""

import datetime  # NOQA

from typing import Any, Dict, List, Optional

from dateutil.tz import tzutc  # NOQA

from switchcraft.conversion import param_list_to_dict
from switchcraft.data_classes.base import DictWrapper


class RdsAssociatedRole:

    def role_arn(self) -> str:
        return self.get('RoleArn')

    def feature_name(self) -> str:
        return self.get('FeatureName')

    def status(self) -> str:
        return self.get('Status')


class RdsListenerEndpoint(DictWrapper):

    @property
    def address(self) -> str:
        return self.get('Address')

    @property
    def port(self) -> int:
        return self.get('Port')

    @property
    def hosted_zone_id(self):
        return self.get('HostedZoneId')


class RdsOptionGroupMembership(DictWrapper):

    @property
    def option_group_name(self) -> str:
        return self.get('OptionGroupName')

    @property
    def status(self) -> str:
        return self.get('Status')


class RdsDBSubnet(DictWrapper):

    @property
    def subnet_identifier(self) -> str:
        return self.get('SubnetIdentifier')

    @property
    def subnet_availability_zone(self) -> str:
        return self.get('SubnetAvailabilityZone')['Name']

    @property
    def subnet_outpost(self):
        # TODO: Implement
        pass

    @property
    def subnet_status(self) -> str:
        return self.get('SubnetStatus')


class RdsDBSubnetGroup(DictWrapper):

    @property
    def db_subnet_group_name(self) -> str:
        return self.get('DBSubnetGroupName')

    @property
    def db_subnet_group_description(self) -> str:
        return self.get('DBSubnetGroupDescription')

    @property
    def vpc_id(self) -> str:
        return self.get('VpcId')

    @property
    def db_subnet_group_status(self) -> str:
        return self.get('SubnetGroupStatus')

    @property
    def subnets(self) -> List[RdsDBSubnet]:
        return [RdsDBSubnet(s) for s in self.get('Subnets')]


class RdsDBParameterGroup(DictWrapper):

    @property
    def db_parameter_group_name(self) -> str:
        """Returns DB Parameter Group Name.

        Ex. default.mysql8.0
        """
        return self.get('DBParameterGroupName')

    @property
    def parameter_apply_status(self) -> str:
        return self.get('ParameterApplyStatus')


class RdsVpcSecurityGroup(DictWrapper):

    @property
    def vpc_security_group_id(self) -> str:
        """Returns the VPC Security Group Id.

        Ex. sg-d9b2ce8d
        """
        return self.get('VpcSecurityGroupId')

    @property
    def status(self) -> str:
        return self.get('Status')


class RdsDBSecurityGroup(DictWrapper):

    @property
    def db_security_group_name(self) -> str:
        return self.get('DBSecurityGroupName')

    @property
    def status(self) -> str:
        return self.get('Status')


class RdsDBEndpoint(DictWrapper):

    @property
    def address(self) -> str:
        return self.get('Address')

    @property
    def port(self) -> int:
        return self.get('Port')

    @property
    def hosted_zone_id(self) -> str:
        return self.get('HostedZoneId')


class RdsDBInstance(DictWrapper):

    @property
    def db_instance_identifier(self) -> str:
        """Returns the Database Instance Id.

        Ex. database-1
        """
        return self.get('DBInstanceIdentifier')

    @property
    def db_instance_class(self) -> str:
        """Returns the database instances class.

        Ex. db.t2.micro
        """
        return self.get('DBInstanceClass')

    @property
    def engine(self) -> str:
        """Returns the engine type defined for the instance.

        Ex. mysql, aurora
        """
        return self.get('Engine')

    @property
    def db_instance_status(self) -> str:
        """Returns the status of the DB instance.

        Ex. available
        """
        return self.get('DBInstanceStatus')

    @property
    def master_username(self) -> str:
        return self.get('MasterUsername')

    @property
    def db_name(self) -> str:
        return self.get('DBName')

    @property
    def endpoint(self) -> RdsDBEndpoint:
        return RdsDBEndpoint(self.get('Endpoint'))

    @property
    def allocated_storage(self) -> int:
        return self.get('AllocatedStorage')

    @property
    def instance_create_time(self) -> str:
        create_time = self.get('InstanceCreateTime')
        return create_time.strftime('%d-%b-%Y %H:%M:%S')

    @property
    def preferred_backup_window(self) -> str:
        """Returns the preferred backup window defined for the instance.

        Ex. 10:17-10:47
        """
        return self.get('PreferredBackupWindow')

    @property
    def backup_retention_period(self) -> int:

        return self.get('BackupRetentionPeriod')

    @property
    def db_security_groups(self) -> List[RdsDBSecurityGroup]:
        return [RdsDBSecurityGroup(g) for g in self.get('DBSecurityGroups')]

    @property
    def vpc_security_groups(self) -> List[RdsVpcSecurityGroup]:
        return [RdsVpcSecurityGroup(g) for g in self.get('VpcSecurityGroups')]

    @property
    def db_parameter_groups(self) -> List[RdsDBParameterGroup]:
        return [RdsDBParameterGroup(g) for g in self.get('DBParameterGroups')]

    @property
    def availability_zone(self) -> str:
        return self.get('AvailabilityZone')

    @property
    def db_subnet_group(self) -> RdsDBSubnetGroup:
        return RdsDBSubnetGroup(self.get('DBSubnetGroup'))

    @property
    def preferred_maintenance_window(self) -> str:
        return self.get('PreferredMaintenanceWindow')

    @property
    def preferred_modified_values(self) -> dict:
        # TODO: Implement
        pass

    @property
    def multi_az(self) -> bool:
        return self.get('MultiAZ')

    @property
    def engine_version(self) -> str:
        return self.get('EngineVersion')

    @property
    def auto_minor_version_upgrade(self) -> bool:
        return self.get('AutoMinorVersionUpgrade')

    @property
    def read_replica_db_instance_identifiers(self):
        # TODO: Implement
        pass

    @property
    def license_model(self) -> str:
        return self.get('LicenseModel')

    @property
    def option_group_memberships(self) -> List[RdsOptionGroupMembership]:
        memberships = self.get('OptionGroupMemberships')
        return [RdsOptionGroupMembership(m) for m in memberships]

    @property
    def publicly_accessible(self) -> bool:
        return self.get('PubliclyAccessible')

    @property
    def storage_type(self) -> str:
        return self.get('StorageType')

    @property
    def db_instance_port(self) -> int:
        return self.get('DbInstancePort')

    @property
    def storage_encrypted(self) -> bool:
        return self.get('StorageEncrypted')

    @property
    def dbi_resource_id(self) -> str:
        return self.get('DbiResourceId')

    @property
    def ca_certificate_identifier(self) -> str:
        return self.get('CACertificateIdentifier')

    @property
    def domain_memberships(self):
        # TODO: Implement
        pass

    @property
    def copy_tags_to_snapshot(self) -> bool:
        return self.get('CopyTagsToSnapshot')

    @property
    def monitoring_interval(self) -> int:
        return self.get('MonitoringInterval')

    @property
    def db_instance_arn(self) -> str:
        return self.get('DBInstanceArn')

    @property
    def iam_database_authentication_enabled(self) -> bool:
        return self.get('IAMDatabaseAuthenticationEnabled')

    @property
    def performance_insights_enabled(self) -> bool:
        return self.get('PerformanceInsightsEnabled')

    @property
    def deletion_protection(self) -> bool:
        return self.get('DeletionProtection')

    @property
    def associated_roles(self):
        # TODO: Implement
        pass

    @property
    def listener_endpoint(self) -> Optional[RdsListenerEndpoint]:
        return None if RdsListenerEndpoint is None else RdsListenerEndpoint(self.get('ListenerEndpoint'))  # NOQA

    @property
    def max_allocated_storage(self) -> int:
        return self.get('MaxAllocatedStorage')

    @property
    def tag_list(self) -> Dict[str, Any]:
        return param_list_to_dict(self.get('TagList'))
