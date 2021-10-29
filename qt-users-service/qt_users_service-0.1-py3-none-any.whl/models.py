import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    """
    Custom user model to change behaviour of the default user model
    such as validation and required fields.
    """

    first_name = models.CharField(_("first name"), blank=False, null=False, max_length=64)
    last_name = models.CharField(_("last name"), blank=False, null=False, max_length=64)
    username = models.EmailField(_("email address"), unique=True, null=False, blank=False)
    are_guidelines_accepted = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_subscription_paid = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    language = models.ForeignKey(
        "users_language.Language", null=True, blank=True, on_delete=models.SET_NULL, related_name="users"
    )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @classmethod
    def create_user(cls, email=None, password=None, first_name=None, last_name=None, are_guidelines_accepted=None):

        if not first_name:
            raise ValidationError(
                _("You must enter your first name"),
            )

        if not last_name:
            raise ValidationError(
                _("You must enter your last name"),
            )

        if not are_guidelines_accepted:
            raise ValidationError(
                _("You must accept the guidelines to make an account"),
            )

        new_user = cls.objects.create_user(
            username=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            are_guidelines_accepted=are_guidelines_accepted,
        )

        return new_user

    # def is_email_taken():
    #     pass

    @classmethod
    def is_email_taken(cls, email):
        try:
            cls.objects.get(email=email)
            return True
        except User.DoesNotExist:
            return False

    def verify_email():
        pass

    def request_password_reset():
        pass

    def verify_password_reset():
        pass

    def get_jwt_token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }