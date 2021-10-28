# -*- coding: utf-8 -*-
import json
import pathlib
from typing import Optional

import bottle
from pip_services3_rpc.services import RestService
from pip_services3_rpc.services.ISwaggerService import ISwaggerService


class SwaggerService(RestService, ISwaggerService):

    def __init__(self):
        super(SwaggerService, self).__init__()
        self._base_route = 'swagger'
        self.__routes = {}

    def __calculate_file_path(self, file_name: str) -> str:
        return str(pathlib.Path(__file__).parent) + '/../../pip_services3_swagger/swagger-ui/' + file_name

    def __calculate_content_type(self, file_name: str) -> str:
        ext = ''.join(pathlib.Path(file_name).suffixes)

        if ext == '.html':
            return 'text/html'
        elif ext == '.css':
            return 'text/css'
        elif ext == '.js':
            return 'application/javascript'
        elif ext == '.png':
            return 'image/png'
        else:
            return 'text/plain'

    def __check_file_exist(self, file_name: str) -> bool:
        path = self.__calculate_file_path(file_name)
        return pathlib.Path(path).exists()

    def __load_file_content(self, file_name: str) -> str:
        path = self.__calculate_file_path(file_name)
        if 'png' in bottle.response.get_header('Content-Type', ''):
            return bottle.static_file(file_name, path)
        return pathlib.Path(path).read_text(encoding='utf-8')

    def __get_swagger_file(self, file_name: str) -> Optional[str]:
        file_name = file_name.lower()

        if not self.__check_file_exist(file_name):
            bottle.response.status = 404
            return

        bottle.response.set_header('Content-Type', self.__calculate_content_type(file_name))
        content = self.__load_file_content(file_name)
        return content

    def __get_index(self) -> str:
        content = self.__load_file_content('index.html')

        # Inject urls
        urls = []
        for prop in self.__routes:
            url = {
                'name': prop,
                'url': self.__routes[prop]
            }
            urls.append(url)

        content = content.replace('[/*urls*/]', json.dumps(urls))

        bottle.response.set_header('Content-Type', 'text/html')
        return content

    def __redirect_to_index(self):
        url = bottle.request.urlparts.path
        if not url.endswith('/'):
            url = url + '/'

        bottle.redirect(url + 'index.html', 301)

    def __compose_swagger_route(self, base_route: str, route: str) -> str:
        if base_route is not None and base_route != '':
            if route is None or route == '':
                route = '/'
            if not route.startswith('/'):
                route = '/' + route
            if not base_route.startswith('/'):
                base_route = '/' + base_route
            route = base_route + route

        return route

    def register_open_api_spec(self, base_route: str, swagger_route: str = None):
        if swagger_route is None:
            super()._register_open_api_spec(base_route)
        else:
            route = self.__compose_swagger_route(base_route, swagger_route)
            base_route = base_route or 'default'
            self.__routes[base_route] = route

    def register(self):
        # A hack to redirect default base route
        base_route = self._base_route
        self._base_route = None
        self.register_route('get', base_route, None, self.__redirect_to_index)
        self._base_route = base_route

        self.register_route('get', '/', None, self.__redirect_to_index)
        self.register_route('get', '/index.html', None, self.__get_index)
        self.register_route('get', '/<file_name>', None, self.__get_swagger_file)
