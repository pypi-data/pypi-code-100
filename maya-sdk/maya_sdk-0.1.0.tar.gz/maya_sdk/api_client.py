from typing import BinaryIO, TextIO, List, Any
from .client import Client


class AuthenticationClient:
    def __init__(self, api_client):
        self.api_client = api_client

    def login(self, email: str, password: str, google_id_token: str):
        return self.api_client.api_call(
            "post",
            f"/auth/login",
            json={
                "email": email,
                "password": password,
                "google_id_token": google_id_token,
            },
        )

    def refresh_token(self, refresh_token: str):
        return self.api_client.api_call(
            "post", f"/auth/refresh_token", params={"refresh_token": refresh_token}
        )

    def reset_password_request(self, email: str):
        return self.api_client.api_call(
            "post", f"/auth/reset_password_request", json={"email": email}
        )

    def reset_password(self, request_id: str, email: str, new_password: str):
        return self.api_client.api_call(
            "post",
            f"/auth/reset_password",
            json={
                "request_id": request_id,
                "email": email,
                "new_password": new_password,
            },
        )


class UserClient:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_user(
        self,
    ):
        return self.api_client.api_call("get", f"/user")

    def sign_up(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        google_id_token: str,
    ):
        return self.api_client.api_call(
            "post",
            f"/user",
            json={
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "google_id_token": google_id_token,
            },
        )

    def update_user(
        self, first_name: str, last_name: str, company_name: str, company_position: str
    ):
        return self.api_client.api_call(
            "patch",
            f"/user",
            json={
                "first_name": first_name,
                "last_name": last_name,
                "company_name": company_name,
                "company_position": company_position,
            },
        )


class OrganizationsClient:
    def __init__(self, api_client):
        self.api_client = api_client

    def list_organizations(
        self,
    ):
        return self.api_client.api_call("get", f"/organizations")

    def create_organization(self, name: str):
        return self.api_client.api_call("post", f"/organizations", json={"name": name})

    def get_organization(self, organization_id: int):
        return self.api_client.api_call("get", f"/organizations/{organization_id}")

    def list_members(self, organization_id: int):
        return self.api_client.api_call(
            "get", f"/organizations/{organization_id}/users"
        )

    def remove_member(self, user_id: int, organization_id: int):
        return self.api_client.api_call(
            "delete", f"/organizations/{organization_id}/users/{user_id}"
        )


class ServicesClient:
    def __init__(self, api_client):
        self.api_client = api_client

    def list_services(
        self,
    ):
        return self.api_client.api_call("get", f"/services")

    def oauth_start(self, organization_id: int, service_uuid: str):
        return self.api_client.api_call(
            "post",
            f"/services/{service_uuid}/oauth/start",
            params={"organization_id": organization_id},
        )

    def oauth_verify_code(
        self, code: str, state: str, organization_id: int, service_uuid: str
    ):
        return self.api_client.api_call(
            "post",
            f"/services/{service_uuid}/oauth/verify_code",
            params={"code": code, "state": state, "organization_id": organization_id},
        )


class ServiceaccountsClient:
    def __init__(self, api_client):
        self.api_client = api_client

    def list_service_accounts(self, organization_id: int):
        return self.api_client.api_call(
            "get", f"/service_accounts", params={"organization_id": organization_id}
        )

    def connect_service_account(self, credentials_id: str, organization_id: int):
        return self.api_client.api_call(
            "post",
            f"/service_accounts",
            params={
                "credentials_id": credentials_id,
                "organization_id": organization_id,
            },
        )

    def delete_service_account(self, organization_id: int, account_uuid: str):
        return self.api_client.api_call(
            "delete",
            f"/service_accounts/{account_uuid}",
            params={"organization_id": organization_id},
        )


class FilesClient:
    def __init__(self, api_client):
        self.api_client = api_client

    def upload_csv(self, category: str, file: BinaryIO):
        return self.api_client.api_call(
            "post",
            f"/files/upload_csv",
            params={"category": category},
            files={"file": file},
        )


class ClusteringClient:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_wordgroups(self, organization_id: int):
        return self.api_client.api_call(
            "get",
            f"/clustering/wordgroups",
            params={"organization_id": organization_id},
        )

    def put_wordgroups(self, organization_id: int):
        return self.api_client.api_call(
            "put",
            f"/clustering/wordgroups",
            params={"organization_id": organization_id},
        )

    def list_columns(self, organization_id: int, category: str):
        return self.api_client.api_call(
            "get",
            f"/clustering/{category}",
            params={"organization_id": organization_id},
        )

    def get_columns(self, organization_id: int, category: str, column_id: str):
        return self.api_client.api_call(
            "get",
            f"/clustering/{category}/columns/{column_id}",
            params={"organization_id": organization_id},
        )

    def put_column(
        self,
        organization_id: int,
        category: str,
        column_id: str,
        id: str,
        name: str,
        values: List[Any],
        fields: List[Any],
    ):
        return self.api_client.api_call(
            "put",
            f"/clustering/{category}/columns/{column_id}",
            params={"organization_id": organization_id},
            json={"id": id, "name": name, "values": values, "fields": fields},
        )

    def preview_sql(
        self,
        organization_id: int,
        category: str,
        column_id: str,
        id: str,
        name: str,
        values: List[Any],
        fields: List[Any],
    ):
        return self.api_client.api_call(
            "post",
            f"/clustering/{category}/columns/{column_id}/sql",
            params={"organization_id": organization_id},
            json={"id": id, "name": name, "values": values, "fields": fields},
        )

    def column_preview(
        self,
        order_by: str,
        order_direction: str,
        organization_id: int,
        category: str,
        column_id: str,
        id: str,
        name: str,
        values: List[Any],
        fields: List[Any],
    ):
        return self.api_client.api_call(
            "post",
            f"/clustering/{category}/columns/{column_id}/preview",
            params={
                "order_by": order_by,
                "order_direction": order_direction,
                "organization_id": organization_id,
            },
            json={"id": id, "name": name, "values": values, "fields": fields},
        )

    def value_preview(
        self,
        value: str,
        order_by: str,
        order_direction: str,
        organization_id: int,
        category: str,
        column_id: str,
        id: str,
        name: str,
        values: List[Any],
        fields: List[Any],
    ):
        return self.api_client.api_call(
            "post",
            f"/clustering/{category}/columns/{column_id}/preview_value",
            params={
                "value": value,
                "order_by": order_by,
                "order_direction": order_direction,
                "organization_id": organization_id,
            },
            json={"id": id, "name": name, "values": values, "fields": fields},
        )

    def put_columns(self, organization_id: int, category: str):
        return self.api_client.api_call(
            "put",
            f"/clustering/{category}/columns",
            params={"organization_id": organization_id},
        )


class InvitationsClient:
    def __init__(self, api_client):
        self.api_client = api_client

    def list_invitations(self, organization_id: int):
        return self.api_client.api_call(
            "get", f"/invitations", params={"organization_id": organization_id}
        )

    def create_invitation(self, organization_id: int, email: str):
        return self.api_client.api_call(
            "post",
            f"/invitations",
            params={"organization_id": organization_id},
            json={"email": email},
        )

    def delete_invitation(self, organization_id: int, invitation_id: str):
        return self.api_client.api_call(
            "delete",
            f"/invitations/{invitation_id}",
            params={"organization_id": organization_id},
        )

    def accept_invitation(self, invitation_id: str, organization_slug: str):
        return self.api_client.api_call(
            "post",
            f"/invitations/accept",
            json={
                "invitation_id": invitation_id,
                "organization_slug": organization_slug,
            },
        )


class EmbedClient:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_info(self, organization_id: int):
        return self.api_client.api_call(
            "get", f"/embed", params={"organization_id": organization_id}
        )


class CompetitionanalysisClient:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_reports(self, organization_id: int):
        return self.api_client.api_call(
            "get", f"/competition_reports", params={"organization_id": organization_id}
        )

    def create_report(
        self,
        organization_id: int,
        uuid: str,
        account_uuid: str,
        search_terms_number: int,
        order_by: str,
        country_code: str,
        language_code: str,
        filter_column: str,
        filter_value: str,
    ):
        return self.api_client.api_call(
            "post",
            f"/competition_reports",
            params={"organization_id": organization_id},
            json={
                "uuid": uuid,
                "account_uuid": account_uuid,
                "search_terms_number": search_terms_number,
                "order_by": order_by,
                "country_code": country_code,
                "language_code": language_code,
                "filter_column": filter_column,
                "filter_value": filter_value,
            },
        )

    def list_google_search_countries(
        self,
    ):
        return self.api_client.api_call("get", f"/google_search_countries")

    def get_report(self, organization_id: int, report_id: str):
        return self.api_client.api_call(
            "get",
            f"/competition_reports/{report_id}",
            params={"organization_id": organization_id},
        )

    def put_report(
        self,
        organization_id: int,
        report_id: str,
        uuid: str,
        account_uuid: str,
        search_terms_number: int,
        order_by: str,
        country_code: str,
        language_code: str,
        filter_column: str,
        filter_value: str,
    ):
        return self.api_client.api_call(
            "put",
            f"/competition_reports/{report_id}",
            params={"organization_id": organization_id},
            json={
                "uuid": uuid,
                "account_uuid": account_uuid,
                "search_terms_number": search_terms_number,
                "order_by": order_by,
                "country_code": country_code,
                "language_code": language_code,
                "filter_column": filter_column,
                "filter_value": filter_value,
            },
        )

    def delete_report(self, organization_id: int, report_uuid: str):
        return self.api_client.api_call(
            "delete",
            f"/competition_reports/{report_uuid}",
            params={"organization_id": organization_id},
        )


class PagespeedClient:
    def __init__(self, api_client):
        self.api_client = api_client

    def list_urls(self, organization_id: int):
        return self.api_client.api_call(
            "get", f"/pagespeed_urls", params={"organization_id": organization_id}
        )

    def put_urls(self, organization_id: int):
        return self.api_client.api_call(
            "put", f"/pagespeed_urls", params={"organization_id": organization_id}
        )

    def get_top_urls(self, organization_id: int):
        return self.api_client.api_call(
            "get", f"/pagespeed_urls/top", params={"organization_id": organization_id}
        )


client = Client()

authentication = AuthenticationClient(client)

user = UserClient(client)

organizations = OrganizationsClient(client)

services = ServicesClient(client)

service_accounts = ServiceaccountsClient(client)

files = FilesClient(client)

clustering = ClusteringClient(client)

invitations = InvitationsClient(client)

embed = EmbedClient(client)

competition_analysis = CompetitionanalysisClient(client)

pagespeed = PagespeedClient(client)

