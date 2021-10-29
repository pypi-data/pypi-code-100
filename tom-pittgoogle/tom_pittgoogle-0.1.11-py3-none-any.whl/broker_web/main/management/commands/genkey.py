# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Adds command to ``manage.py`` for generating a new secret key"""

import string

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = 'Generates and prints a new secret key'

    @staticmethod
    def gen_secret_key(length=50, chars=None):
        """Generate a secret key for Django

        Args:
            length (int): The length of the key
            chars  (str): Characters to use
        """

        return get_random_string(length, chars)

    def add_arguments(self, parser):
        """Add arguments to a command line parser

        Adds ``len`` and ``chars`` arguments to CLI.

        Args:
            parser: The parser to add arguments to
        """

        parser.add_argument('len', nargs=1, type=int, default=50)

    def handle(self, *args, **options):
        """Handle a command line call for the parent class"""

        length = options['len'][0]
        chars = string.ascii_lowercase + string.digits + string.punctuation
        self.stdout.write(self.gen_secret_key(length, chars))
