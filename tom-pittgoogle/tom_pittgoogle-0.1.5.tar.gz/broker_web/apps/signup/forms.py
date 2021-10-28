# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``forms`` module defines views forms for data entry and query
construction.

.. autosummary::
   :nosignatures:

   broker_web.apps.signup.forms.CustomUserChangeForm
   broker_web.apps.signup.forms.CustomUserCreationForm
"""

from captcha.fields import ReCaptchaField
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser

user_fields = 'email', 'first_name', 'last_name', 'country', 'affiliation'


class CustomUserCreationForm(UserCreationForm):
    """Custom form for creating a new ``CustomUser``"""

    captcha = ReCaptchaField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = user_fields

    def validate(self, value):
        """Check if value consists only of valid emails."""
        print(value)
        super().validate(value)


class CustomUserChangeForm(UserChangeForm):
    """Custom form for modifying user data"""

    class Meta:
        model = CustomUser
        fields = user_fields
