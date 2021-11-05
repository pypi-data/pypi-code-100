from requests import get, post, delete, put
from threading import Thread
from time import sleep

class Gitlab(Thread):
    def __init__(self, gitlab_url : str, group_id : str, token : str = None) -> None:
        Thread.__init__(self)
        self.__gitlab_url = gitlab_url if gitlab_url[-1] != "/" else gitlab_url[:-1]
        self.__headers = {}
        self.__continue = True

        self.__api_url = self.__gitlab_url + "/api/v4"
        self.__groups_path = "/groups"
        self.__projects_path = "/projects"
        self.__variables_path = "/variables"
        self.__group_id = group_id
        self.__projects = {}

        if token != None:
            self.__headers["PRIVATE-TOKEN"] = token
        self.__group_projects_url = self.__api_url + self.__groups_path + f"/{self.__group_id}" + self.__projects_path
    
    @property
    def variables_path(self):
        return self.__variables_path
    
    @property
    def projects_path(self):
        return self.__projects_path
    
    @property
    def api_url(self):
        return self.__api_url

    @property
    def headers(self):
        return self.__headers
    
    @property
    def projects(self):
        return self.__projects

    def get_projects(self):
        page = 1
        while self.__continue and len(response := get(self.__group_projects_url, headers = self.__headers, params = {"simple" : False, "include_subgroups" : True, "page": page, "per_page": 100, "order_by": "name", "sort": "asc"}).json()) > 0:
            for project in response:
                if not project["id"] in self.__projects and not project["archived"] and self.__continue:
                    self.__projects[project["id"]] = Project(gitlab = self, project_id = project["id"], project_name = project["name"])
            page += 1
        return self.__projects
    
    def stop(self):
        self.__continue = False
    
    def run(self):
        while self.__continue:
            self.get_projects()

class Project:
    def __init__(self, gitlab: Gitlab, project_id : int, project_name : str) -> None:
        self.__project_id = project_id
        self.__project_name = project_name
        self.__gitlab = gitlab
        self.__variables_url = self.__gitlab.api_url + self.__gitlab.projects_path + f"/{self.__project_id}" + self.__gitlab.variables_path
        self.__variables = {}
    
    @property
    def project_name(self):
        return self.__project_name
    
    @property
    def variables(self):
        return self.__variables
    
    @property
    def variables_url(self):
        return self.__variables_url
    
    def __str__(self) -> str:
        return f"Project({self.__project_name})"
    
    def __repr__(self) -> str:
        return self.__str__()

    def __get_variables(self):
        params = {"per_page": 100, "page": 1}
        while (len(variables := get(self.__variables_url, headers = self.__gitlab.headers, params = params).json())):
            for variable in variables:
                if not variable["key"] in self.__variables:
                    self.__variables[variable["key"]] = Variable(gitlab = self.__gitlab, project = self, name = variable["key"])
                self.__variables[variable["key"]].add_env(variable["environment_scope"], variable["value"].replace("\n", ""))
            params["page"] += 1
        return self.__variables

    def fetch_project(self):
        th = Thread(target = self.__get_variables)
        th.start()
        return th
    
    def create_variable(self, var_name : str, var_env : str, var_value : str):
        variable_url = self.__variables_url + f"/{var_name}"
        search_params = {"filter[environment_scope]": var_env}
        response = get(variable_url, headers = self.__gitlab.headers, params = search_params)
        if "message" in response.json():
            create_params = {"key": var_name, "value": var_value, "protected": True, "environment_scope": var_env}
            post(self.__variables_url, headers = self.__gitlab.headers, params = create_params)

    def delete_variable(self, var_name: str):
        try:
            del self.__variables[var_name]
        except:
            pass

class Variable:
    def __init__(self, gitlab : Gitlab, project : Project, name : str) -> None:
        self.__gitlab = gitlab
        self.__project = project
        self.__name = name
        self.__variable_url = self.__project.variables_url + f"/{self.__name}"
        self.__envs = {}
    
    def add_env(self, env : str, value : str):
        self.__envs[env] = value
    
    @property
    def envs(self):
        return self.__envs
    
    @property
    def present_envs(self):
        return f"{', '.join(list(self.__envs.keys()))}"

    def get_env_value(self, env):
        if env in self.__envs:
            return self.__envs[env]
        return None
    
    @property
    def name(self):
        return self.__name

    def delete_env(self, env):
        del_params = {"filter[environment_scope]": env}
        delete(self.__variable_url, headers = self.__gitlab.headers, params = del_params)
        try:
            del self.__envs[env]
        except:
            pass
        return len(list(self.__envs.keys())) == 0
    
    def full_delete(self):
        threads = []
        for env in list(self.__envs.keys()):
            threads.append(Thread(target = self.delete_env, args = (env,)))
            threads[-1].start()
        [thread.join() for thread in threads]
        self.__project.delete_variable(self.__name)
    
    def edit(self, env: str, new_value: str):
        edit_params = {"value": new_value, "environment_scope": env, "filter[environment_scope]": env}
        put(self.__variable_url, headers = self.__gitlab.headers, params = edit_params)
        self.__envs[env] = new_value
    
    def create_env(self, var_env : str, var_value : str):
        self.__project.create_variable(self.__name, var_env = var_env, var_value = var_value)

    def __str__(self) -> str:
        return f"{self.__name}({[env_name for env_name in self.__envs]})"
    
    def __repr__(self) -> str:
        return self.__str__()