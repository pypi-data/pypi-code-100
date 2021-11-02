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


class FakeLDAPSearchTests(FakeLDAPTests):

    def test_search_specific(self):
        conn = self._makeOne()
        self._addUser('foo')
        self._addUser('footwo')
        self._addUser('thirdfoo')

        res = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=foo)')
        dn_values = [dn for (dn, attr_dict) in res]
        self.assertEqual(len(dn_values), 1)
        self.assertEqual(dn_values, ['cn=foo,ou=users,dc=localhost'])

    def test_search_specific_leadingspace(self):
        conn = self._makeOne()
        self._addUser('foo')
        self._addUser('footwo')
        self._addUser('thirdfoo')

        res = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn= foo)')
        dn_values = [dn for (dn, attr_dict) in res]
        self.assertEqual(len(dn_values), 1)
        self.assertEqual(dn_values, ['cn=foo,ou=users,dc=localhost'])

    def test_search_specific_trailingspace(self):
        conn = self._makeOne()
        self._addUser('foo')
        self._addUser('footwo')
        self._addUser('thirdfoo')

        res = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=foo )')
        dn_values = [dn for (dn, attr_dict) in res]
        self.assertEqual(len(dn_values), 1)
        self.assertEqual(dn_values, ['cn=foo,ou=users,dc=localhost'])

    def test_search_specific_leadingtrailingspace(self):
        conn = self._makeOne()
        self._addUser('foo')
        self._addUser('footwo')
        self._addUser('thirdfoo')

        res = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn= foo )')
        dn_values = [dn for (dn, attr_dict) in res]
        self.assertEqual(len(dn_values), 1)
        self.assertEqual(dn_values, ['cn=foo,ou=users,dc=localhost'])

    def test_search_nonspecific(self):
        conn = self._makeOne()
        self._addUser('foo')
        self._addUser('bar')
        self._addUser('baz')

        res = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(objectClass=*)')
        dn_values = [dn for (dn, attr_dict) in res]
        self.assertEqual(set(dn_values),
                         {'ou=users,dc=localhost',
                          'cn=bar,ou=users,dc=localhost',
                          'cn=foo,ou=users,dc=localhost',
                          'cn=baz,ou=users,dc=localhost'})

    def test_search_nonspecific_scope_base(self):
        conn = self._makeOne()
        user_dn, password = self._addUser('foo')

        res = conn.search_s(user_dn,
                            ldap.SCOPE_BASE,
                            filterstr='(objectClass=*)')
        dn_values = [dn for (dn, attr_dict) in res]
        self.assertEqual(len(dn_values), 1)
        self.assertEqual(dn_values, ['cn=foo,ou=users,dc=localhost'])

    def test_search_specific_scope_base(self):
        conn = self._makeOne()
        user_dn, password = self._addUser('foo')

        res = conn.search_s(user_dn,
                            ldap.SCOPE_BASE,
                            filterstr='(&(objectClass=inetOrgPerson)(cn=foo))')
        dn_values = [dn for (dn, attr_dict) in res]
        self.assertEqual(len(dn_values), 1)
        self.assertEqual(dn_values, ['cn=foo,ou=users,dc=localhost'])

    def test_search_full_wildcard(self):
        conn = self._makeOne()
        self._addUser('foo')
        self._addUser('footwo')
        self._addUser('threefoo')

        res = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=*)')
        dn_values = [dn for (dn, attr_dict) in res]
        self.assertEqual(len(dn_values), 3)
        self.assertEqual(set(dn_values),
                         {'cn=foo,ou=users,dc=localhost',
                          'cn=footwo,ou=users,dc=localhost',
                          'cn=threefoo,ou=users,dc=localhost'})

    def test_search_startswithendswith_wildcard(self):
        conn = self._makeOne()
        self._addUser('foo')
        self._addUser('onefootwo')
        self._addUser('threefoo')
        self._addUser('bar')

        res = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=*foo*)')
        dn_values = [dn for (dn, attr_dict) in res]
        self.assertEqual(len(dn_values), 3)
        self.assertEqual(set(dn_values),
                         {'cn=foo,ou=users,dc=localhost',
                          'cn=onefootwo,ou=users,dc=localhost',
                          'cn=threefoo,ou=users,dc=localhost'})

    def test_search_endswith_wildcard(self):
        conn = self._makeOne()
        self._addUser('foo')
        self._addUser('footwo')
        self._addUser('threefoo')

        res = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=*foo)')
        dn_values = [dn for (dn, attr_dict) in res]
        self.assertEqual(len(dn_values), 2)
        self.assertEqual(set(dn_values),
                         {'cn=foo,ou=users,dc=localhost',
                          'cn=threefoo,ou=users,dc=localhost'})

    def test_search_startswith_wildcard(self):
        conn = self._makeOne()
        self._addUser('foo')
        self._addUser('footwo')
        self._addUser('threefoo')

        res = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=foo*)')
        dn_values = [dn for (dn, attr_dict) in res]
        self.assertEqual(len(dn_values), 2)
        self.assertEqual(set(dn_values),
                         {'cn=foo,ou=users,dc=localhost',
                          'cn=footwo,ou=users,dc=localhost'})

    def test_search_anded_filter(self):
        conn = self._makeOne()
        self._addUser('foo')
        self._addUser('bar')
        self._addUser('baz')

        query_success = '(&(cn=foo)(objectClass=inetOrgPerson))'
        res = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr=query_success)
        dn_values = [dn for (dn, attr_dict) in res]
        self.assertEqual(len(dn_values), 1)
        self.assertEqual(dn_values, ['cn=foo,ou=users,dc=localhost'])

        query_failure = '(&(cn=foo)(objectClass=organizationalUnit))'
        self.assertFalse(conn.search_s('ou=users,dc=localhost',
                         ldap.SCOPE_SUBTREE,
                         filterstr=query_failure))

    def test_search_ored_filter(self):
        conn = self._makeOne()
        self._addUser('foo')
        self._addUser('bar')
        self._addUser('baz')

        res = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(|(cn=foo)(cn=bar))')
        dn_values = [dn for (dn, attr_dict) in res]
        self.assertEqual(len(dn_values), 2)
        self.assertEqual(set(dn_values),
                         {'cn=foo,ou=users,dc=localhost',
                          'cn=bar,ou=users,dc=localhost'})

    def test_search_invalid_base(self):
        conn = self._makeOne()
        self._addUser('foo')
        self.assertRaises(ldap.NO_SUCH_OBJECT, conn.search_s,
                          'o=base', ldap.SCOPE_SUBTREE,
                          filterstr='(objectClass=*)')

    def test_search_by_mail(self):
        conn = self._makeOne()
        self._addUser('foo', mail=b'foo@foo.com')
        self._addUser('bar', mail=b'bar@bar.com')
        self._addUser('baz', mail=b'baz@baz.com')

        res = conn.search_s(
            'ou=users,dc=localhost',
            ldap.SCOPE_SUBTREE,
            filterstr='(|(mail=foo@foo.com)(mail=bar@bar.com))')
        dn_values = [dn for (dn, attr_dict) in res]
        self.assertEqual(len(dn_values), 2)
        self.assertEqual(set(dn_values),
                         {'cn=foo,ou=users,dc=localhost',
                          'cn=bar,ou=users,dc=localhost'})

    def test_search_by_utf8(self):
        conn = self._makeOne()
        username1 = 'f\xf8\xf8'
        username2 = 'b\xe5r'
        self._addUser(username1)
        self._addUser(username2)
        self._addUser('baz')

        res = conn.search_s(
            'ou=users,dc=localhost',
            ldap.SCOPE_SUBTREE,
            filterstr='(|(cn=%s)(cn=%s))' % (username1, username2))
        dn_values = [dn for (dn, attr_dict) in res]
        self.assertEqual(len(dn_values), 2)
        self.assertEqual(set(dn_values),
                         {'cn=%s,ou=users,dc=localhost' % username1,
                          'cn=%s,ou=users,dc=localhost' % username2})

    def test_return_all_attributes(self):
        conn = self._makeOne()
        self._addUser('foo', mail=b'foo@foo.com')

        res = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=foo)',
                            attrlist=None)
        self.assertEqual(len(res), 1)
        dn, attr_dict = res[0]
        self.assertEqual(dn, 'cn=foo,ou=users,dc=localhost')
        self.assertTrue('cn' in attr_dict)
        self.assertTrue('mail' in attr_dict)
        self.assertTrue('userPassword' in attr_dict)
        self.assertTrue('objectClass' in attr_dict)

    def test_return_filtered_attributes(self):
        conn = self._makeOne()
        self._addUser('foo', mail=b'foo@foo.com')

        res = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=foo)',
                            attrlist=['cn', 'mail'])
        self.assertEqual(len(res), 1)
        dn, attr_dict = res[0]
        self.assertEqual(dn, 'cn=foo,ou=users,dc=localhost')
        self.assertTrue('cn' in attr_dict)
        self.assertTrue('mail' in attr_dict)
        self.assertFalse('userPassword' in attr_dict)
        self.assertFalse('objectClass' in attr_dict)


@unittest.skipIf(RealLDAPTests is object, 'LDAP server tests not available')
class RealLDAPSearchTest(FakeLDAPSearchTests, RealLDAPTests):
    pass
