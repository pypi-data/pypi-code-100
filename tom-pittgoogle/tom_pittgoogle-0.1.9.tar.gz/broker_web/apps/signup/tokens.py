# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Custom token generation for user signup tasks"""

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return user.pk + timestamp + user.is_active


account_activation_token = TokenGenerator()
