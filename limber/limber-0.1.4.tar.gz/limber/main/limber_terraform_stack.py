from constructs import Construct
from cdktf import TerraformStack, TerraformVariable
from limber.imports.google import (
    GoogleProvider,
    StorageBucket,
    SecretManagerSecret,
    SecretManagerSecretVersion
)
import os
import glob
import json
import importlib
import sys
import hashlib
from limber.main.dag.dag import DAG
from limber.operators.operator import Operator


class LimberTerraformStack(TerraformStack):

    def __init__(self, scope: Construct, ns, project_id, region, cloud_storage_bucket, cloud_storage_bucket_location, folder) -> None:
        super().__init__(scope, ns)

        self.folder = folder

        GoogleProvider(self, id=ns, region=region, project=project_id)

        self.storage_bucket = StorageBucket(
            self,
            "cloud_storage_bucket",
            name=cloud_storage_bucket,
            location=cloud_storage_bucket_location
        )

        #self.get_secrets()
        self.create_terraform_configuration()

    def get_secrets(self):

        secrets = json.loads(os.environ["TERRAFORM_SECRETS"])

        for secret_name in secrets:

            secret_id = f"{secret_name}-secret"
            secret_version = f"{secret_name}-version"

            secret = SecretManagerSecret(
                self,
                secret_id,
                secret_id=secret_id,
                replication={
                    "automatic": True
                }
            )

            variable = TerraformVariable(
                self,
                secret_name,
                type="string",
                sensitive=True,
            )

            SecretManagerSecretVersion(
                self,
                secret_version,
                secret=secret.id,
                secret_data=variable.string_value,
            )

    def create_terraform_configuration(self):

        top_level_dags = self._get_objects(DAG)
        self._get_terraform_configuration_dags(top_level_dags)

    def _get_terraform_configuration_dags(self, dags) -> None:

        for dag in dags:
            dag.get_terraform_json(stack=self)

            tasks = self._get_objects(Operator)
            dag_tasks = [task for task in tasks if task.dag.dag_id == dag.dag_id]

            for task in dag_tasks:
                task.get_terraform_json(stack=self, folder=self.folder, cloud_storage_bucket=self.storage_bucket)

    def _get_objects(self, object_type) -> []:

        files = glob.glob("dags/*.py")

        mods = []

        for filepath in files:
            org_mod_name, _ = os.path.splitext(os.path.split(filepath)[-1])
            path_hash = hashlib.sha1(filepath.encode('utf-8')).hexdigest()
            mod_name = f'unusual_prefix_{path_hash}_{org_mod_name}'

            loader = importlib.machinery.SourceFileLoader(mod_name, filepath)
            spec = importlib.util.spec_from_loader(mod_name, loader)
            new_module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = new_module
            loader.exec_module(new_module)
            mods.append(new_module)

        top_level_dags = [
            o
            for m in mods
            for o in list(m.__dict__.values())
            if isinstance(o, object_type)
        ]

        return top_level_dags
