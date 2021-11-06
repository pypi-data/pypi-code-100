from influxdb_client import BucketsApi, Bucket, Authorization


class Buckets(BucketsApi):
    def __init__(self, client):
        self.org = client.org
        self.authorizations_api = client.authorizations_api
        self.organizations_api = client.organizations_api
        super().__init__(client)

    def _create_bucket(self, bucket_name: str, description: str = None, org_name: str = None) -> Bucket:
        if org_name is None:
            org_name = self.org
        org = self.organizations_api().get_organization(org_name=org_name)
        return self.create_bucket(bucket_name=bucket_name, org=org, description=description)

    def bucket_exists(self, bucket_name):
        return bool(self.find_bucket_by_name(bucket_name))

    def create_bucket_with_auth(self, bucket_name: str, description: str = None,
                                org_name: str = None) -> Authorization:
        """
        Create new bucket with authorization
        :param bucket_name: bucket name
        :param description: bucket description
        :param org_name: organization name
        :return: token
        """

        if org_name is None:
            org_name = self.org

        org = self.organizations_api().get_organization(org_name=org_name)
        bucket = self._create_bucket(bucket_name=bucket_name, description=description, org_name=org_name)
        permissions_read = {
            'action': 'read',
            'resource': {
                'id': bucket.id,
                'name': bucket.name,
                'org': org.name,
                'org_id': org.id,
                'type': 'buckets'
            }
        }
        permissions_write = {
            'action': 'write',
            'resource': {
                'id': bucket.id,
                'name': bucket.name,
                'org': org.name,
                'org_id': org.id,
                'type': 'buckets'
            }
        }
        permissions = [permissions_read, permissions_write]
        authorization = Authorization(org_id=org.id, permissions=permissions, description=description)
        return self.authorizations_api().create_authorization(authorization=authorization)

    def delete_permissions(self, bucket_name, org=None, read=True, write=True, delete_if_none=True):
        if org is None:
            org = self.org

        organization = self.organizations_api().get_organization_by_name(org_name=org)
        auths = self.authorizations_api().find_authorizations_by_org(organization)
        for auth in auths:
            orig_perm = list(auth.permissions)
            for perm in auth.permissions:
                if locals()[perm.action]:
                    if perm.resource.name == bucket_name:
                        perm.resource.name = None
                        # auth.permissions[perm]
                        # auth.permissions.remove(perm)
            if orig_perm != auth.permissions:
                self.authorizations_api().update_authorization(auth=auth)
            if delete_if_none:
                if all([bool(i.resource.name is None and i.resource.id is not None) for i in auth.permissions]):
                    self.authorizations_api().delete_authorization(auth=auth)

    def delete_bucket_by_name(self, bucket_name: str):
        bucket = self.find_bucket_by_name(bucket_name)
        print('bucket', bucket, bucket_name)
        self.delete_bucket(bucket=bucket)
