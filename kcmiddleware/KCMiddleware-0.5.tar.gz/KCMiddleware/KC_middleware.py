import re
import logging
from django.conf import settings
from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from keycloak.exceptions import KeycloakInvalidTokenError, KeycloakAuthorizationConfigError, KeycloakError
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotAuthenticated, NotFound
from . import KC_exceptions
from .KC_utils import KeycloakService
from .KC_models import KeycloakUser
import jwt
import json

logger = logging.getLogger(__name__)


class KeycloakMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        """
        :param get_response:
        """

        self.keycloak_authorization_config = settings.KEYCLOAK_CONFIG.get('KEYCLOAK_AUTHORIZATION_CONFIG', None)
        self.default_access = settings.KEYCLOAK_CONFIG.get('KEYCLOAK_DEFAULT_ACCESS', "DENY")
        self.method_validate_token = settings.KEYCLOAK_CONFIG.get('KEYCLOAK_METHOD_VALIDATE_TOKEN', "INTROSPECT")

        # Create Keycloak instance
        self.keycloak = KeycloakService.connect_authentication_client()

        # Read policies
        if self.keycloak_authorization_config:
            self.keycloak.load_authorization_config(self.keycloak_authorization_config)

        # Django
        self.get_response = get_response

    @property
    def keycloak_authorization_config(self):
        return self._keycloak_authorization_config

    @keycloak_authorization_config.setter
    def keycloak_authorization_config(self, value):
        self._keycloak_authorization_config = value

    def __call__(self, request):
        """
        :param request:
        :return:
        """
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Validate only the token introspect.
        :param request: django request
        :param view_func:
        :param view_args: view args
        :param view_kwargs: view kwargs
        :return:
        """
        if hasattr(settings, 'KEYCLOAK_BEARER_AUTHENTICATION_EXEMPT_PATHS'):
            path = request.path_info.lstrip('/')

            if any(re.match(m, path) for m in
                   settings.KEYCLOAK_BEARER_AUTHENTICATION_EXEMPT_PATHS):
                logger.debug('** exclude path found, skipping')
                return None

        try:
            view_scopes = view_func.cls.keycloak_scopes
        except AttributeError:
            logger.debug(
                'Allowing free access, since no authorization configuration (keycloak_scopes) found for this request '
                'route :%s',
                request)
            return None

        if 'HTTP_AUTHORIZATION' not in request.META:
            return JsonResponse({"detail": NotAuthenticated.default_detail},
                                status=NotAuthenticated.status_code)

        auth_header = request.META.get('HTTP_AUTHORIZATION').split()
        token = auth_header[1] if len(auth_header) == 2 else auth_header[0]

        if 'KEYCLOAK_INTROSPECT_OFFLINE' in settings.KEYCLOAK_CONFIG and \
                self.parse_boolean(settings.KEYCLOAK_CONFIG['KEYCLOAK_INTROSPECT_OFFLINE']):
            token_introspected = jwt.decode(token, options={"verify_signature": False})
        else:
            token_introspected = self.keycloak.introspect(token)

        if self.is_user_active(token_introspected) is False:
            return JsonResponse({"detail": 'Token expired'},
                                status=AuthenticationFailed.status_code)

        try:
            # userinfo = KeycloakService().userinfo(token)

            client = self.extract_client(request)

            # Momentarily needed both `user` and `_user`
            user_ = self.craft_user(token, token_introspected, client)
            request._user = user_
            request.user = user_

            # Get the required scope needed by the endpoint
            required_scope = view_scopes.get(request.method, None) \
                if view_scopes.get(request.method, None) else view_scopes.get('DEFAULT', None)

            if required_scope == 'open':
                return None

            # DEFAULT scope not found and DEFAULT_ACCESS is DENY
            if not required_scope and self.default_access == 'DENY':
                return JsonResponse({"detail": PermissionDenied.default_detail}, status=PermissionDenied.status_code)

            user_permissions = self.get_permissions(token_introspected, client['company_slug'])

        except KeycloakInvalidTokenError:
            return JsonResponse({"detail": AuthenticationFailed.default_detail},
                                status=AuthenticationFailed.status_code)
        except KC_exceptions.JWTError as error:
            return JsonResponse({"detail": str(error)},
                                status=AuthenticationFailed.status_code)
        except KC_exceptions.ExpiredSignatureError as error:
            return JsonResponse({"detail": str(error)},
                                status=AuthenticationFailed.status_code)
        except KC_exceptions.JWTClaimsError as error:
            return JsonResponse({"detail": str(error) + ' | check https://stackoverflow.com/a/53627747/10158519'},
                                status=AuthenticationFailed.status_code)
        except NotFound:
            return JsonResponse({"detail": 'Client not found'},
                                status=NotFound.status_code)

        except KeycloakError as e:
            return JsonResponse({"detail": json.loads(e.error_message)['error']},
                                status=e.response_code)

        except KeyError as e:
            return JsonResponse(
                {"detail": 'To Access this endpoint an Id-Client is required in the header of the request'},
                status=406)

        scope = required_scope

        if type(required_scope) is dict:
            scope = required_scope['scope']
            if required_scope['service_scope'] not in user_.current_client['optional_client_scopes']:
                return JsonResponse({"detail": PermissionDenied.default_detail},
                                    status=PermissionDenied.status_code)

        # Tries to match the permission of the user and the scope of the endpoint
        if user_permissions is not None:
            for perm in user_permissions:
                if scope in perm.scopes:
                    return None

        # User Permission Denied
        return JsonResponse({"detail": PermissionDenied.default_detail},
                            status=PermissionDenied.status_code)

    def get_permissions(self, userinfo, company_slug):
        """
        Get permission by user token

        :param client_id:
        :param userinfo:
        :return permissions list:
        """

        if not self.keycloak.authorization.policies:
            raise KeycloakAuthorizationConfigError(
                "Keycloak settings not found. Load Authorization Keycloak settings."
            )

        user_resources = userinfo['resource_access'].get(company_slug)

        if not user_resources:
            return None

        permissions = []

        for policy_name, policy in self.keycloak.authorization.policies.items():
            for role in user_resources['roles']:
                if self.keycloak._build_name_role(role) in policy.roles:
                    permissions += policy.permissions

        return list(set(permissions))

    def extract_client(self, request):
        detail_url_names = ['company-detail']
        no_auth_url_names = ['company-list', 'user-info']

        if request.resolver_match.url_name in no_auth_url_names:
            return {'company_slug': self.keycloak.client_id}

        elif request.resolver_match.url_name in detail_url_names:
            try:
                return KeycloakService().get_company_by_client_id(request.resolver_match.kwargs['pk'])
            except KC_exceptions.KeycloakCompanyDoesNotExist:
                raise NotFound
        else:
            # if 'Id-client' not in request.headers:
            #     raise KC_exceptions.IdClientRequired
            try:
                id_client = request.headers['Id-Client']
                return KeycloakService().get_company_by_client_id(id_client)
            except KC_exceptions.KeycloakCompanyDoesNotExist:
                raise NotFound

    def craft_user(self, tk, userinfo, current_client):
        """
        It creates a user obj from the token in order
        to inject it into the request.

        :param current_client:
        :param tk:
        :param userinfo:
        :return User object:
        """
        return KeycloakUser(userinfo['sub'],
                            userinfo['email'],
                            userinfo['given_name'],
                            userinfo['family_name'],
                            userinfo,
                            tk,
                            current_client)

    def is_user_active(self, token_introspect):
        return token_introspect['active']

    def parse_boolean(self, b):
        return b == "True" or b == "true"
