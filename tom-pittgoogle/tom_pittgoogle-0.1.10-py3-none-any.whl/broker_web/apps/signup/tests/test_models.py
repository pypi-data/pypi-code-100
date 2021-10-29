# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``models`` and ``managers`` modules"""

from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserManager(TestCase):
    """Test user creation"""

    def test_create_user(self):
        """Test creation of regular user has correct defaults"""

        user_model = get_user_model()

        test_email = 'test@user.com'
        new_user = user_model.objects.create_user(email=test_email, password='test')

        self.assertEqual(new_user.email, test_email, 'Email does not equal passed value.')
        self.assertFalse(new_user.is_active, 'User is set to active')
        self.assertFalse(new_user.is_staff, 'User is staff')
        self.assertFalse(new_user.is_superuser, 'User is superuser')

        with self.assertRaises(TypeError, msg='No error raised for missing email'):
            user_model.objects.create_user()

        with self.assertRaises(TypeError, msg='No error raised for blank email'):
            user_model.objects.create_user(email='')

    def test_create_superuser(self):
        """Test creation of a superuser has correct defaults"""

        user_model = get_user_model()

        test_email = 'test@user.com'
        new_admin_user = user_model.objects.create_superuser(test_email, 'foo')

        self.assertEqual(new_admin_user.email, test_email, 'Email does not equal passed value.')
        self.assertTrue(new_admin_user.is_active, 'User is not active')
        self.assertTrue(new_admin_user.is_staff, 'User is not staff')
        self.assertTrue(new_admin_user.is_superuser, 'User is not superuser')

        with self.assertRaises(TypeError, msg='No error raised for missing email'):
            user_model.objects.create_superuser()

        with self.assertRaises(TypeError, msg='No error raised for blank email'):
            user_model.objects.create_superuser(email='')

        with self.assertRaises(ValueError, msg='No error raised for is_superuser=False'):
            user_model.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)
