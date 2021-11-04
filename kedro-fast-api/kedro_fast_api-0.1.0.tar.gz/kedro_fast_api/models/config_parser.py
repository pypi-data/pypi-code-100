import yaml


class ConfigParser:
    def __init__(self, path: str) -> None:
        self.config_dict = self._read_yml(path)
        self.security = self.config_dict.get('security')
        self.only_kedro = self.config_dict.get('only_kedro')
        self.routes = self._get_routes()

    def _read_yml(self, catalog_path):
        with open(catalog_path, 'r') as stream:
            try:
                return(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                raise exc

    def _get_routes(self):
        try:
            # self._validate_routes()
            if self.only_kedro:
                return {}
            return self.config_dict.get('routes')
        except KeyError:
            raise Exception('Make sure to add "routes" key to model file')