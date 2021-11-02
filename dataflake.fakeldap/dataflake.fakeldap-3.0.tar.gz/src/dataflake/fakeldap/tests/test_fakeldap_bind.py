##############################################################################
#
# Copyright (c) 2008-2021 Jens Vagelpohl and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import unittest

import ldap

from .base import FakeLDAPTests
from .base import RealLDAPTests


class FakeLDAPBindTests(FakeLDAPTests):

    def test_bind_empty_pwd(self):
        # Empty passwords are disallowed
        conn = self._makeOne()

        self.assertRaises(ldap.UNWILLING_TO_PERFORM,
                          conn.simple_bind_s,
                          'cn=Anybody',
                          '')

    def test_bind_manager(self):
        conn = self._makeOne()

        # special case for logging in as "Manager"
        # only applies to FakeLDAP connection objects
        self.assertTrue(conn.simple_bind_s('cn=Manager', 'whatever'))
        self.assertEqual(conn.whoami_s(), 'dn:cn=Manager')

    def test_bind_success(self):
        conn = self._makeOne()
        user_dn, password = self._addUser('foo')

        # Login with correct credentials
        self.assertTrue(conn.simple_bind_s(user_dn, password))
        self.assertEqual(conn.whoami_s(), 'dn:%s' % user_dn)

    def test_bind_wrong_pwd(self):
        conn = self._makeOne()
        user_dn, password = self._addUser('foo')

        # Login with bad credentials
        self.assertRaises(ldap.INVALID_CREDENTIALS, conn.simple_bind_s,
                          user_dn, 'INVALID PASSWORD')

    def test_bind_no_password_in_record(self):
        conn = self._makeOne()
        conn.simple_bind_s(self._rootdn, self._rootpw)

        # Users with empty passwords cannot log in
        encoded_name = b'user2'
        user2 = [('cn', [encoded_name]),
                 ('sn', [encoded_name]),
                 ('objectClass', [b'top', b'person'])]
        conn.add_s('cn=user2,ou=users,dc=localhost', user2)
        self.assertRaises(ldap.INVALID_CREDENTIALS, conn.simple_bind_s,
                          'cn=user2,ou=users,dc=localhost', 'ANY PASSWORD')

    def test_bind_no_such_user(self):
        conn = self._makeOne()
        conn.simple_bind_s(self._rootdn, self._rootpw)

        encoded_name = b'user2'
        user2 = [('cn', [encoded_name]),
                 ('sn', [encoded_name]),
                 ('userPassword', [b'foo']),
                 ('objectClass', [b'top', b'person'])]
        conn.add_s('cn=user2,ou=users,dc=localhost', user2)
        self.assertRaises(ldap.INVALID_CREDENTIALS, conn.simple_bind_s,
                          'cn=user1,ou=users,dc=localhost', 'ANY PASSWORD')

    def test_unbind_clears_last_bind(self):
        conn = self._makeOne()
        user_dn, password = self._addUser('foo')

        self.assertTrue(conn.simple_bind_s(user_dn, password))
        self.assertEqual(conn.whoami_s(), 'dn:%s' % user_dn)

        conn.unbind()
        self.assertRaises(Exception, conn.whoami_s)

    def test_unbind_s_clears_last_bind(self):
        conn = self._makeOne()
        user_dn, password = self._addUser('foo')

        self.assertTrue(conn.simple_bind_s(user_dn, password))
        self.assertEqual(conn.whoami_s(), 'dn:%s' % user_dn)

        conn.unbind_s()
        self.assertRaises(Exception, conn.whoami_s)


@unittest.skipIf(RealLDAPTests is object, 'LDAP server tests not available')
class RealLDAPBindTests(FakeLDAPBindTests, RealLDAPTests):

    @unittest.skip('Only applicable for FakeLDAP connection')
    def test_bind_manager(self):
        pass


class HashedPasswordTests(FakeLDAPTests):

    def test_connection_is_hashed(self):
        conn = self._makeOne()
        self.assertEqual(conn.hash_password, True)

    def test_password_is_hashed(self):
        from ..utils import hash_pwd
        conn = self._makeOne()
        self._addUser('foo')

        res = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=foo)')
        pwd = res[0][1]['userPassword'][0]
        self.assertEqual(pwd, hash_pwd('foo_secret'))

    def test_bind_success(self):
        conn = self._makeOne()
        user_dn, password = self._addUser('foo')

        # Login with correct credentials
        self.assertTrue(conn.simple_bind_s(user_dn, password))
        self.assertEqual(conn.whoami_s(), 'dn:%s' % user_dn)

    def test_bind_wrong_pwd(self):
        conn = self._makeOne()
        user_dn, password = self._addUser('foo')

        # Login with bad credentials
        self.assertRaises(ldap.INVALID_CREDENTIALS, conn.simple_bind_s,
                          user_dn, 'INVALID PASSWORD')


@unittest.skipIf(RealLDAPTests is object, 'LDAP server tests not available')
class RealLDAPHashedPasswordTests(HashedPasswordTests, RealLDAPTests):
    pass


class ClearTextPasswordTests(FakeLDAPTests):

    def _getTargetClass(self):
        from .. import FakeLDAPConnection

        class ClearTextConnection(FakeLDAPConnection):
            """ A FakeLDAPConnection with password hashing disabled
            """
            hash_password = False

        return ClearTextConnection

    def test_connection_is_clear_text(self):
        conn = self._makeOne()
        self.assertEqual(conn.hash_password, False)

    def test_password_is_clear_text(self):
        conn = self._makeOne()
        user_dn, password = self._addUser('foo')

        res = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=foo)')
        pwd = res[0][1]['userPassword'][0]
        self.assertEqual(pwd, b'foo_secret')

    def test_bind_success(self):
        conn = self._makeOne()
        user_dn, password = self._addUser('foo')

        # Login with correct credentials
        self.assertEqual(user_dn, 'cn=foo,ou=users,dc=localhost')
        self.assertEqual(password, b'foo_secret')
        self.assertTrue(conn.simple_bind_s(user_dn, password))
        self.assertEqual(conn.whoami_s(), 'dn:%s' % user_dn)

    def test_bind_wrong_pwd(self):
        conn = self._makeOne()
        user_dn, password = self._addUser('foo')

        # Login with bad credentials
        self.assertRaises(ldap.INVALID_CREDENTIALS, conn.simple_bind_s,
                          user_dn, 'INVALID PASSWORD')
