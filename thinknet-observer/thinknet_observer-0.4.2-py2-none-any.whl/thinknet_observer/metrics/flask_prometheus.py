# import typing as t

# from prometheus_client import make_wsgi_app
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from werkzeug.middleware.dispatcher import DispatcherMiddleware


# class FlaskPrometheus(Flask):
#     def __init__(
#         self,
#         import_name: str,
#         static_url_path: t.Optional[str] = None,
#         static_folder: t.Optional[str] = "static",
#         static_host: t.Optional[str] = None,
#         host_matching: bool = False,
#         subdomain_matching: bool = False,
#         template_folder: t.Optional[str] = "templates",
#         instance_path: t.Optional[str] = None,
#         instance_relative_config: bool = False,
#         root_path: t.Optional[str] = None,
#     ):

#         super().__init__(
#             import_name,
#             static_url_path=static_url_path,
#             static_folder=static_folder,
#             static_host=static_host,
#             host_matching=host_matching,
#             subdomain_matching=subdomain_matching,
#             template_folder=template_folder,
#             instance_path=instance_path,
#             instance_relative_config=instance_relative_config,
#             root_path=root_path,
#         )

#         # add middleware
#         self.wsgi_app = DispatcherMiddleware(
#             self.wsgi_app, {"/metrics": make_wsgi_app()}
#         )

#     def route(self, rule: str, **options: t.Any) -> t.Callable:
#         return super().route(rule, **options)


# # app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})
