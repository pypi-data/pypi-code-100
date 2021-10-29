from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.settings import (NAME_MAX_LENGTH, PASSWORD_MAX_LENGTH,
                            PASSWORD_MIN_LENGTH)
from users_auth.validators import email_not_taken_validator


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[email_not_taken_validator])
    password = serializers.CharField(
        min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH, validators=[validate_password]
    )
    are_guidelines_accepted = serializers.BooleanField()
    first_name = serializers.CharField(max_length=NAME_MAX_LENGTH, allow_blank=False)
    last_name = serializers.CharField(max_length=NAME_MAX_LENGTH, allow_blank=False)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(allow_blank=False)
    password = serializers.CharField(min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH)
