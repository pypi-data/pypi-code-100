from django.contrib.auth import authenticate
from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from users_auth.serializers import LoginSerializer, RegisterSerializer
from users_common.utils.model_loaders import get_user_model


class Register(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.valid_request_data(serializer.validated_data)

    def valid_request_data(self, data):
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")
        are_guidelines_accepted = data.get("are_guidelines_accepted")

        User = get_user_model()

        new_user = User.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            are_guidelines_accepted=are_guidelines_accepted,
        )

        with transaction.atomic():
            new_user.save()

        return Response(_("Account succesfully registered"), status=status.HTTP_201_CREATED)


class EmailVerification(APIView):
    pass


class Login(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.valid_request_data(serializer.validated_data)

    def valid_request_data(self, data):
        email = data["email"]
        password = data["password"]
        user = authenticate(username=email, password=password)
        if user is not None:
            token = user.get_jwt_token()
            # token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token}, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed()


class PasswordResetRequest(APIView):
    pass


class PasswordResetVerify(APIView):
    pass
