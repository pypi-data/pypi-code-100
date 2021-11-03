import abc

import requests

from whizbang.core.workflow_task import WorkflowTask, IWorkflowTask
from whizbang.domain.manager.az.az_account_manager import AzAccountManager
from whizbang.domain.manager.databricks.databricks_cluster_manager import IDatabricksClusterManager
from whizbang.domain.manager.databricks.databricks_job_manager import IDatabricksJobManager
from whizbang.domain.manager.databricks.databricks_library_manager import IDatabricksLibraryManager
from whizbang.domain.manager.databricks.databricks_secret_scope_manager import IDatabricksSecretScopeManager
from whizbang.domain.manager.databricks.databricks_workspace_manager import IDatabricksWorkspaceManager
from whizbang.domain.manager.databricks.databricks_pool_manager import IDatabricksPoolManager
from whizbang.domain.models.databricks.databricks_cluster import DatabricksCluster
from whizbang.domain.models.databricks.databricks_job import DatabricksJob
from whizbang.domain.models.databricks.databricks_library import DatabricksLibrary
from whizbang.domain.models.databricks.databricks_notebook import DatabricksNotebook
from whizbang.domain.models.databricks.databricks_pool import DatabricksPool
from whizbang.domain.models.databricks.databricks_state import DatabricksState
from whizbang.domain.workflow.verify_deployed_workflow_task import VerifyDeployedWorkflowTask


class IDatabricksTask(IWorkflowTask):

    @abc.abstractmethod
    def run(self, request: DatabricksState):
        """"""


class CreatePoolsTask(VerifyDeployedWorkflowTask, IDatabricksTask):
    def __init__(self, manager: IDatabricksPoolManager):
        WorkflowTask.__init__(self)
        self.manager = manager

    @property
    def task_name(self) -> str:
        return "create_pools"

    def run(self, request: DatabricksState):
        def __run(request: DatabricksState):
            for pool_json in request.pool_state:
                try:
                    self.manager.save(request.client, DatabricksPool(pool_json))
                except KeyError as e:
                    print(f'pool json not properly formatted: {e}')

        self.verify_deployed(callback=__run, resource_name="Databricks Workspace", timeout_seconds=300, request=request)


class UpdateClusterSecretScopeTask(WorkflowTask, IDatabricksTask):
    def __init__(self, manager: IDatabricksSecretScopeManager, account_manager: AzAccountManager):
        WorkflowTask.__init__(self)
        self.manager = manager
        self.account_manager = account_manager

    @property
    def task_name(self) -> str:
        return "set cluster secret scope"

    def run(self, request: DatabricksState):
        if self.account_manager.get_account().account_type.lower() == 'serviceprincipal':
            print('A service principal cannot create a databricks secret scope, skipping secret scope creation...')
            return
        self.manager.save(client_args=request.client, t_object=request.secret_scope)


class CreateClustersTask(WorkflowTask, IDatabricksTask):
    def __init__(self, manager: IDatabricksClusterManager):
        WorkflowTask.__init__(self)
        self.manager = manager

    @property
    def task_name(self) -> str:
        return "create_clusters"

    def run(self, request: DatabricksState):
        for cluster_json in request.cluster_state:
            try:
                self.manager.update_secret_scope_env_variable(secret_scope=request.secret_scope,
                                                              cluster=cluster_json)
                self.manager.save(request.client, DatabricksCluster(cluster_json))
            except KeyError as e:
                print(f'cluster json not properly formatted: {e}')
            except requests.HTTPError:
                print(f'{cluster_json["cluster_name"]} could not be started')


class PinClustersTask(WorkflowTask, IDatabricksTask):
    def __init__(self, manager: IDatabricksClusterManager):
        WorkflowTask.__init__(self)
        self.manager = manager

    @property
    def task_name(self) -> str:
        return "pin_clusters"

    def run(self, request: DatabricksState):
        for cluster_json in request.cluster_state:
            try:
                self.manager.pin_cluster(client_args=request.client, cluster=DatabricksCluster(cluster_json))
            except KeyError as e:
                print(f'cluster json not properly formatted: {e}')


class CreateNotebooksTask(WorkflowTask, IDatabricksTask):
    def __init__(self, manager: IDatabricksWorkspaceManager):
        WorkflowTask.__init__(self)
        self.manager = manager

    @property
    def task_name(self) -> str:
        return "create_notebooks"

    def run(self, request: DatabricksState) -> any:
        self.manager.save(request.client, DatabricksNotebook(source_path=request.notebook_state))


class CreateLibrariesTask(WorkflowTask, IDatabricksTask):
    def __init__(self, manager: IDatabricksLibraryManager):
        WorkflowTask.__init__(self)
        self.manager = manager

    @property
    def task_name(self) -> str:
        return "create_libraries"

    def run(self, request: DatabricksState) -> any:
        for library in request.universal_library_state:
            try:
                self.manager.save(request.client, DatabricksLibrary(library_dict=library, install_all=True))
            except KeyError as e:
                print(f'all cluster library json not properly formatted: {e}')
            except requests.HTTPError:
                print(f'{library} could not be installed on all clusters')
        for target_cluster_libraries in request.library_state:
            try:
                self.manager.save(request.client, DatabricksLibrary(library_dict=target_cluster_libraries))
            except KeyError as e:
                print(f'library json not properly formatted: {e}')
            except requests.HTTPError:
                print(f'libraries could not be installed on'
                      f' {target_cluster_libraries["cluster_name"]}')


class CreateJobsTask(WorkflowTask, IDatabricksTask):
    def __init__(self, manager: IDatabricksJobManager):
        WorkflowTask.__init__(self)
        self.manager = manager

    @property
    def task_name(self) -> str:
        return "create_jobs"

    def run(self, request: DatabricksState):
        for job_json in request.job_state:
            try:
                self.manager.save(request.client, DatabricksJob(job_json['settings']))
            except KeyError as e:
                print(f'job json not properly formatted: {e}')
            except requests.HTTPError:
                print(f'{job_json["settings"]["name"]} could not be installed on the cluster'
                      f' {job_json["settings"]["existing_cluster_name"]}')
