from rest_framework.exceptions import APIException
from rest_framework import status
from django.conf import settings


class StandardError(Exception):
    pass


class JWTError(StandardError):
    pass


class JWTClaimsError(JWTError):
    pass


class ExpiredSignatureError(JWTError):
    pass


class UserDoesntBelongToCompanyException(APIException):
    def __init__(self):
        UserDoesntBelongToCompanyException.status_code = status.HTTP_406_NOT_ACCEPTABLE
        UserDoesntBelongToCompanyException.detail = 'The user_id does not belong to the company.'


class KeycloakUserExist(APIException):
    def __init__(self):
        KeycloakUserExist.status_code = status.HTTP_409_CONFLICT
        KeycloakUserExist.detail = 'A user with this credentials already exists'


class KeycloakCompanyDoesNotExist(APIException):
    def __init__(self):
        KeycloakCompanyDoesNotExist.status_code = status.HTTP_404_NOT_FOUND
        KeycloakCompanyDoesNotExist.detail = 'This company id does not exist!'


class CompanyNotCreated(APIException):
    def __init__(self):
        CompanyNotCreated.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        CompanyNotCreated.detail = 'Company could not be created.'


class RoleDoesNotExist(APIException):
    def __init__(self):
        RoleDoesNotExist.status_code = status.HTTP_406_NOT_ACCEPTABLE
        RoleDoesNotExist.detail = f'The role provided doesn\'t exist. The roles accepted are: {settings.ROLES}'


class UserDoesNotExist(APIException):
    def __init__(self):
        UserDoesNotExist.status_code = status.HTTP_406_NOT_ACCEPTABLE
        UserDoesNotExist.detail = 'The user_id provided doesn\'t exist.'


class IdClientRequired(KeyError):
    def __init__(self):
        IdClientRequired.status_code = status.HTTP_406_NOT_ACCEPTABLE
        IdClientRequired.detail = 'To Access this endpoint an Id-client is required in the header of the request'


class RandomException(APIException):
    def __init__(self, text, status_code):
        RandomException.status_code = status_code
        RandomException.detail = text