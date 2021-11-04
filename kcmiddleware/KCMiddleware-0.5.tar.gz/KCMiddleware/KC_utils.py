from typing import Union
from keycloak import KeycloakAdmin, KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakGetError
from django.conf import settings
from .KC_exceptions import UserDoesNotExist


class KeycloakService:
    def __init__(self) -> None:
        self.admin: KeycloakAdmin = KeycloakService.connect_admin()
        self.authentication_client: KeycloakOpenID = KeycloakService.connect_authentication_client()

    @staticmethod
    def connect_admin():
        return KeycloakAdmin(
            server_url=settings.KEYCLOAK_CONFIG['KEYCLOAK_SERVER_URL'],
            realm_name=settings.KEYCLOAK_CONFIG['KEYCLOAK_REALM'],
            username=settings.KEYCLOAK_CONFIG['KEYCLOAK_ADMIN_USERNAME'],
            password=settings.KEYCLOAK_CONFIG['KEYCLOAK_ADMIN_PASSWORD'],
            user_realm_name=settings.KEYCLOAK_CONFIG['KEYCLOAK_REALM'],
            client_id=settings.KEYCLOAK_CONFIG['KEYCLOAK_CLIENT_AUTHENTICATION_ID'],
            client_secret_key=settings.KEYCLOAK_CONFIG['KEYCLOAK_CLIENT_AUTHENTICATION_SECRET'],
            verify=True)

    def refresh_admin(self):
        self.admin = KeycloakService.connect_admin()

    def __refresh_if_needed_and_exec__(self, function, **kwargs):
        try:
            return function(**kwargs)
        except KeycloakAuthenticationError:
            self.refresh_admin()
            return function(**kwargs)

    def create_user(self, user_data, id_client=None, client_role=None):

        """
        :param client_roles:
        :param user_data:
        :return:

        user_obj is an instance of UserRepresentation
        Docs: https://www.keycloak.org/docs-api/5.0/rest-api/index.html#_userrepresentation
        """

        exist = self.__refresh_if_needed_and_exec__(self.admin.get_user_id, username=user_data['email'])
        user_id = exist
        if not exist:
            # raise KeycloakUserExist
            user_obj = {
                "email": user_data['email'],
                "username": user_data['email'],
                "enabled": True,
                "firstName": user_data['first_name'],
                "lastName": user_data['last_name'],
                "credentials": [
                    {
                        "value": user_data['password'],
                        "type": "password",
                        "temporary": False
                    }
                ],
                "attributes": {
                    "telephone": [user_data['telephone']],
                }
            }

            user_id = self.__refresh_if_needed_and_exec__(self.admin.create_user, payload=user_obj)
            KeycloakService().assign_client_role(user_id,
                                                 settings.KEYCLOAK_CONFIG["KEYCLOAK_CLIENT_AUTHENTICATION_INTERNAL_ID"],
                                                 f'APP_{settings.KEYCLOAK_CONFIG["KEYCLOAK_APPLICATION_ID"]}')

        if client_role is not None:
            # Apparently is not possible to set roles during user creation (Bummer)
            # https://stackoverflow.com/questions/49818453/client-roles-havent-assigned-during-creating-new-user-in-keycloak
            KeycloakService().assign_client_role(user_id, id_client,
                                                 f'{client_role}_{settings.KEYCLOAK_CONFIG["KEYCLOAK_APPLICATION_ID"]}')
            KeycloakService().assign_client_role(user_id, id_client,
                                                 f'APP_{settings.KEYCLOAK_CONFIG["KEYCLOAK_APPLICATION_ID"]}')

        return user_id

    def get_user_id(self, username: str) -> Union[str, None]:
        return self.__refresh_if_needed_and_exec__(self.admin.get_user_id, username=username)

    def get_user(self, user_id: str) -> Union[str, None]:
        try:
            return self.__refresh_if_needed_and_exec__(self.admin.get_user, user_id=user_id)
        except KeycloakGetError:
            raise UserDoesNotExist

    def set_enabled_and_verified(self, user_id) -> None:
        pass
        # TODO
        # payload = {
        #     'enabled': True,
        #     'emailVerified': True
        # }
        # return self.__refresh_if_needed_and_exec__(self.admin.update_user, user_id=user_id, payload=payload)

    def set_new_password(self, user_id, password, temporary) -> bool:
        # TODO check if works
        return self.__refresh_if_needed_and_exec__(self.admin.set_user_password, user_id=user_id, password=password,
                                                   temporary=temporary)
        # try:
        #     self.admin.set_user_password(user_id=user_id, password=password, temporary=temporary)
        # except KeycloakAuthenticationError:  # for when token is expired
        #     self.refresh_admin()
        #     self.admin.set_user_password(user_id=user_id, password=password, temporary=temporary)
        # except Exception as e:
        #     print(e)
        #     return False
        # return True

    def update_user(self, first_name: str, last_name: str, email: str, telephone: str, keycloak_id: str) -> Union[str, None]:
        payload = {
            'firstName': first_name,
            'lastName': last_name,
            'email': email,
            'username': email,
            'attributes': {
                'telephone': [telephone],
            }
        }
        return self.__refresh_if_needed_and_exec__(
            self.admin.update_user, user_id=keycloak_id, payload=payload
        )

    def get_members_in_company(self, client_id):

        return self.__refresh_if_needed_and_exec__(self.admin.get_client_role_members,
                                                   client_id=client_id,
                                                   role_name=f'APP_{settings.KEYCLOAK_CONFIG["KEYCLOAK_APPLICATION_ID"]}')

    def get_members_in_role(self, client_id, role_name):
        role_name += '_' + settings.KEYCLOAK_CONFIG["KEYCLOAK_APPLICATION_ID"]
        return self.__refresh_if_needed_and_exec__(self.admin.get_client_role_members,
                                                   client_id=client_id,
                                                   role_name=role_name)

    def get_client_roles_of_user(self, user_id, client_id):
        return self.__refresh_if_needed_and_exec__(self.admin.get_client_roles_of_user,
                                                   user_id=user_id,
                                                   client_id=client_id)

    def create_company_and_set_settings(self, user_id, payload):
        client_id = None
        try:
            company_slug = self.create_company(payload)
            client_id = KeycloakService().get_company_by_client_name(company_slug)
            KeycloakService().create_client_roles(client_id=client_id)
            KeycloakService().assign_client_role(user_id, client_id, 'COMPANY_OWNER')
            KeycloakService().assign_client_role(user_id, client_id,
                                                 f'APP_{settings.KEYCLOAK_CONFIG["KEYCLOAK_APPLICATION_ID"]}')

        except Exception as error:
            print(error)
            if client_id is not None:
                KeycloakService().admin.delete_client(client_id)
            raise KeycloakGetError
        return client_id

    def create_company(self, payload, id_company=1):
        # TODO move scope settings somewhere else
        # payload['clientId'] = 'company_' + str(id_company) + '_' + payload['name'].replace(' ', '_').lower()
        payload['clientId'] = 'ZE_' + str(id_company).rjust(4, '0')
        payload['authorizationServicesEnabled'] = True
        payload['serviceAccountsEnabled'] = True

        try:
            self.__refresh_if_needed_and_exec__(self.admin.create_client,
                                                payload=payload)
            return payload['clientId']
        except KeycloakGetError as error:
            print(error)
            if error.response_code == 409:
                id_company += 1
                return self.create_company(payload, id_company=id_company)
            raise KeycloakGetError

    def update_company(self, client_id, payload):
        self.__refresh_if_needed_and_exec__(self.admin.update_client,
                                            client_id=client_id,
                                            payload=payload)

    def create_client_roles(self, client_id):
        """
        Creates a unique `COMPANY_OWNER` role for the client
        and 10 dummy roles for each sub role

        :param client_id:
        :return:
        """

        sub_roles = settings.ROLES + ['APP']

        payload = {'name': 'COMPANY_OWNER'}
        self.__refresh_if_needed_and_exec__(self.admin.create_client_role,
                                            client_role_id=client_id,
                                            payload=payload)

        for role in sub_roles:
            for i in range(10):
                payload = {'name': role + f'_{i}'}
                self.__refresh_if_needed_and_exec__(self.admin.create_client_role,
                                                    client_role_id=client_id,
                                                    payload=payload)

    def get_company_by_client_name(self, client_name):
        return self.__refresh_if_needed_and_exec__(self.admin.get_client_id,
                                                   client_name=client_name)

    def get_companies_related_to_user(self, access_token, user_info=None):
        companies = []
        if user_info is None:
            user_info = self.userinfo(access_token)
        for resource, value in user_info['resource_access'].items():
            if resource.startswith('company') or resource.startswith('ZE'):
                client_id = self.get_company_by_client_name(resource)
                client = self.get_company_by_client_id(client_id=client_id)
                client['roles'] = value['roles']
                companies.append(client)
        return companies

    def get_company_by_client_id(self, client_id):
        client = self.__refresh_if_needed_and_exec__(self.admin.get_client,
                                                     client_id=client_id)
        return {"id_client": client['id'],
                "company_slug": client['clientId'],
                "name": client['name'],
                "description": client['description'],
                "optional_client_scopes": client['optionalClientScopes']}

    def assign_client_role(self, user_id: str, client_id: str, role: str):
        role = self.admin.get_client_role(client_id, role)
        return self.__refresh_if_needed_and_exec__(self.admin.assign_client_role,
                                                   user_id=user_id,
                                                   client_id=client_id,
                                                   roles=role)

    def remove_client_role(self, user_id: str, client_id: str, roles: str):
        role = self.admin.get_client_role(client_id, roles)
        return self.__refresh_if_needed_and_exec__(self.admin.delete_client_roles_of_user,
                                                   user_id=user_id,
                                                   client_id=client_id,
                                                   roles=role)

    def get_user_client_role(self, user_id: str, client_id: str):
        return self.__refresh_if_needed_and_exec__(self.admin.get_client_roles_of_user,
                                                   user_id=user_id,
                                                   client_id=client_id)

    def change_client_role(self, user_id: str, client_id: str, role: str):
        current_roles = self.get_user_client_role(user_id, client_id)
        for item in current_roles:
            self.remove_client_role(user_id, client_id, item['name'])

        if role != 'COMPANY_OWNER':
            role = f'{role}_{settings.KEYCLOAK_CONFIG["KEYCLOAK_APPLICATION_ID"]}'
        app_role = f'APP_{settings.KEYCLOAK_CONFIG["KEYCLOAK_APPLICATION_ID"]}'

        self.assign_client_role(user_id, client_id, app_role)
        return self.assign_client_role(user_id, client_id, role)

    @staticmethod
    def connect_authentication_client():
        return KeycloakOpenID(server_url=settings.KEYCLOAK_CONFIG['KEYCLOAK_SERVER_URL'],
                              client_id=settings.KEYCLOAK_CONFIG['KEYCLOAK_CLIENT_AUTHENTICATION_ID'],
                              realm_name=settings.KEYCLOAK_CONFIG['KEYCLOAK_REALM'],
                              client_secret_key=settings.KEYCLOAK_CONFIG['KEYCLOAK_CLIENT_AUTHENTICATION_SECRET'])

    def login_user(self, user_dict):
        return self.authentication_client.token(user_dict['email'], user_dict['password'])

    def refresh_token(self, token_dict):
        return self.authentication_client.refresh_token(token_dict['refresh_token'])

    def userinfo(self, token):
        return self.authentication_client.userinfo(token)

    def logout(self, token_dict):
        return self.authentication_client.logout(token_dict['refresh_token'])

    def set_enabled(self, user_id, enabled) -> None:
        payload = {
            'enabled': enabled
        }
        return self.__refresh_if_needed_and_exec__(self.admin.update_user, user_id=user_id, payload=payload)
