import json
from typing import List

from drone_api_client.model.cron import DroneCron
from .model.build import Build
from .model.repos import DroneRepo
from .model.secrets import DroneSecret
from .model.template import DroneTemplate
from .model.user import DroneUser
from .service import get_dict_from_locals
from .session import Session


class Base:
    def __init__(self, session):
        self._session: Session = session

    def _valid(self, response, return_class, key: str = None, add_session: bool = False):
        if isinstance(response, str):
            return response
        elif key:
            return return_class(response[key]) if isinstance(response[key], dict) else \
                [return_class(elem) for elem in response[key]]
        else:
            if add_session:
                return return_class(self, response) if isinstance(response, dict) else \
                    [return_class(self, elem) for elem in response]
            else:
                return return_class(response) if isinstance(response, dict) else [return_class(elem) for elem in
                                                                                  response]


class Cron(Base):
    def create_cron(self, name: str, expr: str, branch: str = 'master') -> DroneCron:
        """
        https://docs.drone.io/api/cron/cron_create/

        Create a new cron job. Please note this api requires write access to the repository
        :param name: name of cron job
        :param expr: cron expression
        :param branch: branch were cron will be runs
        :return: DroneCron object with created cron job
        """
        data = get_dict_from_locals(locals())
        return self._valid(self._session.request('post', '/cron', data=data), DroneCron)

    def delete_cron(self, cron_name: str) -> None:
        """
        https://docs.drone.io/api/cron/cron_delete/

        Deletes a cron job. Please note this api requires write access to the repository
        :param cron_name: existing cron in repository
        :return: None
        """
        return self._session.request('delete', f'/cron/{cron_name}')

    def get_cron_info(self, cron_name: str) -> DroneCron:
        """
        https://docs.drone.io/api/cron/cron_info/

        Returns the named cron job. Please note this api requires write access to the repository
        :param cron_name: existing cron name
        :return: DroneCron object if cron exists
        """
        return self._valid(self._session.request('get', f'/cron/{cron_name}'), DroneCron)

    def get_cron_list(self) -> List[DroneCron]:
        """
        https://docs.drone.io/api/cron/cron_list/

        Returns the cron job list. Please note this api requires write access to the repository
        :return: Returns list of all cron jobs in repository
        """
        return self._valid(self._session.request('get', '/cron'), DroneCron)

    def execute(self, cron_name: str) -> DroneCron:
        """
        https://docs.drone.io/api/cron/cron_trigger/

        Trigger an existing cron task. Please note this api requires write access to the repository
        :param cron_name: existing cron name
        :return: executed cron
        """
        return self._valid(self._session.request('post', f'/cron/{cron_name}'), DroneCron)

    def update_cron(self, name: str, expr: str = None, branch: str = None) -> DroneCron:
        """
        https://docs.drone.io/api/cron/cron_update/

        Updates the named cron job. Please note this api requires write access to the repository
        :param name: existing crone name
        :param expr: new cron expression. Optional
        :param branch: new branch. Optional
        :return: Updated cron
        """
        cron = self.get_cron_info(name)
        if isinstance(cron, (list, tuple)):
            return "Cron expression with given name doesn't found"
        cron.expr = expr if expr else cron.expr
        cron.branch = branch if branch else cron.branch
        return self._valid(self._session.request('patch', f'/cron/{name}', data=cron.to_dict()), DroneCron)


class Secrets(Base):
    def create(self, name: str, data: str, pull_request: bool = True) -> DroneSecret:
        """
        https://docs.drone.io/api/secrets/secret_create/

        Create a new repository secret. Please note this api requires write access to the repository
        :param name: new secret name
        :param data: data for secret
        :param pull_request:
        :return: DroneSecret object with created secret
        """
        data = get_dict_from_locals(locals(), exclude=['name'])
        return self._valid(self._session.request('post', '/secrets', data=data), DroneSecret)

    def delete(self, secret_name: str) -> None:
        """
        https://docs.drone.io/api/secrets/secret_delete/

        Deletes a repository secret. Please note this api requires write access to the repository
        :param secret_name:
        :return: None
        """
        return self._session.request('delete', f'/secrets/{secret_name}')

    def get_secret_info(self, secret_name: str) -> DroneSecret:
        """
        https://docs.drone.io/api/secrets/secret_info/

        Returns the repository secret.
        Please note this api requires write access to the repository,
        and the request parameter {secret} is not the secret’s id but secret name
        :param secret_name: existing secret name
        :return: DroneSecret object if secrets found in repository
        """
        return self._valid(self._session.request('get', f'/secrets/{secret_name}'), DroneSecret)

    def get_secrets(self) -> List[DroneSecret]:
        """
        https://docs.drone.io/api/secrets/secret_list/

        Returns the repository secret list. Please note this api requires write access to the repository
        :return: List of DroneSecret in repo
        """
        return self._valid(self._session.request('get', '/secrets'), DroneSecret)

    def update_secret(self, secret_name: str, data: str = None, pull_request: bool = None) -> DroneSecret:
        """
        https://docs.drone.io/api/secrets/secret_update/

        Updates the specified repository secret.
        Please note this api requires write access to the repository,
        and the request parameter {secret} is not the secret’s id but secret name.
        :param secret_name: existing secret
        :param data: new data in secret
        :param pull_request: bool value
        :return: DroneSecret object
        """

        secret = self.get_secret_info(secret_name)
        if isinstance(secret, (list, tuple)):
            return "Secret with given name doesn't found"
        data = get_dict_from_locals(locals(), exclude=['name'])
        return self._valid(self._session.request('patch', f'/secrets/{secret.name}', data=data), DroneSecret)


class User(Base):
    def get_user_builds(self) -> List[Build]:
        """
        https://docs.drone.io/api/user/user_builds/

        Returns the currently authenticated user’s build feed
        :return:
        """
        return self._valid(self._session.request('get', '/user/builds', add_repo=False), Build)

    def get_user_info(self) -> DroneUser:
        """
        https://docs.drone.io/api/user/user_info/

        Returns the currently authenticated user
        :return: Current drone user
        """
        return self._valid(self._session.request('get', '/user', add_repo=False), DroneUser)

    def get_user_repos(self) -> List[DroneRepo]:
        """
        https://docs.drone.io/api/user/user_repos/

        :return: Returns the currently authenticated user’s repository list
        """
        return self._valid(self._session.request('get', '/user/repos', add_repo=False), DroneUser)

    def sync_user_repos_list(self) -> None:
        """
        https://docs.drone.io/api/user/user_sync/

        Synchronize the currently authenticated user’s repository list.
        :return: None
        """
        self._session.request('post', '/user/repos', add_repo=False)


class Users(Base):
    def create_user(self, login: str, email: str, active: bool = True, avatar_url: str = '') -> DroneUser:
        """
        https://docs.drone.io/api/users/users_create/

        Creates a user. Please note this api requires administrative privileges.
        :param login: login for new user
        :param email: email for new user
        :param active: is active user. Default is True
        :param avatar_url: link to user avatar. Default is ''
        :return: created user
        """
        data = DroneUser(get_dict_from_locals(locals())).to_create()
        return self._valid(self._session.request('post', '/users', data=data, add_repo=False), DroneUser)

    def delete_user(self, login: str) -> None:
        """
        https://docs.drone.io/api/users/users_delete/

        Deletes a user. Please note this api requires administrative privileges.
        :param login: existing user login
        :return: None
        """
        self._session.request('delete', f'/users/{login}', add_repo=False)

    def get_user_info(self, login: str) -> DroneUser:
        """
        https://docs.drone.io/api/users/users_info/

        Returns information about the named registered user. Please note this api requires administrative privileges.
        :param login: existing user login
        :return: DroneUser object with user
        """
        return self._valid(self._session.request('get', f'/users/{login}', add_repo=False), DroneUser)

    def get_users_list(self) -> List[DroneUser]:
        """
        https://docs.drone.io/api/users/users_list/

        Returns a list of all registered users. Please note this api requires administrative privileges.
        :return: List of users
        """
        return self._valid(self._session.request('get', '/users', add_repo=False), DroneUser)


class Repos(Base):
    def disable_repo(self, repo_name: str) -> DroneRepo:
        """
        https://docs.drone.io/api/repos/repo_delete/

        Permanently deletes a repository. It cannot be undone.
        Please note this api requires administrative access to the repository,
        and repository’s secrets and builds aren’t deleted
        :param repo_name: existing repo name
        :return: DroneRepo object
        """
        return self._valid(self._session.request('delete', f'/repos/{repo_name}', add_repo=False), DroneRepo)

    def enable_repo(self, repo_name: str) -> DroneRepo:
        """
        https://docs.drone.io/api/repos/repo_create/

        Registers a named repository with Drone. Please note this api requires administrative access to the repository
        :param repo_name: existing repo name
        :return: DroneRepo object
        """
        return self._valid(self._session.request('post', f'/repos/{repo_name}', add_repo=False), DroneRepo)

    def get_repo_info(self, repo_name: str) -> DroneRepo:
        """
        https://docs.drone.io/api/repos/repo_info/

        Retrieves the details of a repository. Please note this api requires read access to the repository.
        :param repo_name: existing repository name
        :return: DroneRepo object
        """
        return self._valid(self._session.request('get', f'/repos/{repo_name}', add_repo=False), DroneRepo)

    def repo_list(self) -> List[DroneRepo]:
        """
        https://docs.drone.io/api/repos/repo_list/

        :return: repositories which are registered to Drone
        """
        return self._valid(self._session.request('get', '/user/repos', add_repo=False), DroneRepo)

    def repair_repo(self, repo_name: str) -> None:
        """
        https://docs.drone.io/api/repos/repo_repair/

        Recreates webhooks for your repository in your version control system (e.g GitHub).
        This can be used if you accidentally delete your webhooks.
        Please note this api requires administrative access to the repository
        :param repo_name: existing repo name
        :return: None
        """
        return self._valid(self._session.request('post', f'/repos/{repo_name}/repair', add_repo=False), DroneRepo)

    def update(self, repo_name: str, dict_with_update: dict) -> DroneRepo:
        """
        https://docs.drone.io/api/repos/repo_update/

        Updates a named repository. Please note this api requires administrative access to the repository
        :param repo_name: existing repo name
        :param dict_with_update: dict with updated parameters
        :return: updated DroneRepo object
        """
        repos = self.get_repo_info(repo_name)
        if isinstance(repos, (list, tuple)):
            return f"Can't find {repo_name}"
        else:
            data = json.dumps({key: value for key, value in dict_with_update if key in DroneRepo.__change__})
            return self._valid(self._session.request('patch', f'/repos/{repo_name}', add_repo=False, data=data),
                               DroneRepo)


class Template(Base):
    def create(self, name: str, data: str, namespace: str) -> DroneTemplate:
        """
        https://docs.drone.io/api/templates/template_create/

        Create a new template. Please note this api requires write access to the repository
        :param name: template name
        :param data: template data
        :param namespace: template namespace
        :return: DroneTemplate object
        """
        data = get_dict_from_locals(locals())
        return self._valid(self._session.request('post', '/templates', data=data, add_repo=False), DroneTemplate)

    def delete(self, namespace: str, name: str) -> None:
        """
        https://docs.drone.io/api/templates/template_delete/

        Deletes a template. Please note this api requires write access to the repository
        :param namespace: existing namespace name
        :param name: existing template name
        :return: None
        """
        self._session.request('delete', f'/templates/{namespace}/{name}', add_repo=False)

    def get_template_info(self, namespace: str, name: str) -> DroneTemplate:
        """
        https://docs.drone.io/api/templates/template_info/

        Returns the template. Please note this api requires write access to the repository
        :param namespace: existing namespace name
        :param name: existing template name
        :return:
        """
        return self._valid(self._session.request('get', f'/templates/{namespace}/{name}', add_repo=False),
                           DroneTemplate)

    def get_template_list(self, namespace: str):
        """
        https://docs.drone.io/api/templates/template_list/

        Returns the organization template list. Please note this api requires write access to the repository
        :return:
        """
        return self._valid(self._session.request('get', f'/templates/{namespace}', add_repo=False), DroneTemplate)


class Builds(Base):
    def build_approve(self, build_number: int):
        """
        https://docs.drone.io/api/builds/build_approve/

        Approves a blocked build. Please note this api requires write access to the repository,
        and the request parameter {build} is not the build id but the build number.
        :param build_number: is not the build id but the build number.
        :return:
        """
        self._session.request('post', f'/builds/{build_number}/approve')

    def build_decline(self, build_number: int):
        """
        https://docs.drone.io/api/builds/build_approve/

        Declines a blocked build. Please note this api requires write access to the repository,
        and the request parameter {build} is not the build id but the build number.
        :param build_number: is not the build id but the build number.
        :return:
        """
        self._session.request('post', f'/builds/{build_number}/decline')

    def build_info(self, build_number: int) -> Build:
        """
        https://docs.drone.io/api/builds/build_info/

        Returns the specified repository build. Please note this api requires read access to the repository
        and the request parameter {build} is not the build id but the build number.
        :param build_number: is not the build id but the build number.
        :return:
        """
        return self._valid(self._session.request('get', f'/builds/{build_number}'), Build)

    def build_list(self) -> List[Build]:
        """
        https://docs.drone.io/api/builds/build_list/

        Returns recent builds for the repository based on name.
        Please note this api requires read access to the repository

        :return:
        """
        return self._valid(self._session.request('get', '/builds'), Build)

    def build_logs(self, build_number: int):
        """
        https://docs.drone.io/api/builds/build_logs/

        Please note this api requires read access to the repository
        :param build_number: is not the build id but the build number.
        :return:
        """
        return self._session.request('get', f'/builds/{build_number}/logs/')

    def build_restart(self, build_number: int) -> Build:
        """
        https://docs.drone.io/api/builds/build_start/

        Restart the specified build. Please note this api requires read and write access to the repository
        and the request parameter {build} is not the build id but the build number.
        :param build_number: is not the build id but the build number.
        :return:
        """
        return self._valid(self._session.request('post', f'/builds/{build_number}'), Build)

    def build_stop(self, build_number: int) -> Build:
        """
        https://docs.drone.io/api/builds/build_stop/

        Stop the specified build. Please note this api requires administrative privileges
        and the request parameter {build} is not the build id but the build number.
        :param build_number: is not the build id but the build number.
        :return:
        """
        return self._valid(self._session.request('delete', f'/builds/{build_number}'), Build)
