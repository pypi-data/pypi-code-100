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


class FakeLDAPModifyTests(FakeLDAPTests):

    def test_modify_wrongbase(self):
        conn = self._makeOne()
        self.assertRaises(ldap.UNWILLING_TO_PERFORM, conn.modify_s,
                          'cn=foo,o=base', [])

    def test_modify_wrongrecord(self):
        conn = self._makeOne()
        self._addUser('foo')

        conn.simple_bind_s(self._rootdn, self._rootpw)
        self.assertRaises(ldap.NO_SUCH_OBJECT, conn.modify_s,
                          'cn=bar,ou=users,dc=localhost', [])

    def test_modify_success(self):
        import copy
        from ldap.modlist import modifyModlist
        conn = self._makeOne()
        self._addUser('foo')

        foo = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=foo)')
        old_values = foo[0][1]
        self.assertEqual(old_values['objectClass'], [b'top', b'inetOrgPerson'])
        self.assertFalse(old_values.get('mail'))
        new_values = copy.deepcopy(old_values)
        new_values['description'] = [b'foo@email.com']

        modlist = modifyModlist(old_values, new_values)
        conn.simple_bind_s(self._rootdn, self._rootpw)
        conn.modify_s('cn=foo,ou=users,dc=localhost', modlist)
        foo = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=foo)')
        self.assertEqual(foo[0][1]['description'], [b'foo@email.com'])

    def test_modify_replace(self):

        conn = self._makeOne()
        self._addUser('foo', mail=b'foo@bar.com')

        foo = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=foo)')
        old_values = foo[0][1]
        self.assertEqual(old_values['mail'], [b'foo@bar.com'])

        modlist = [(ldap.MOD_REPLACE, 'mail', [b'foo@email.com'])]
        conn.simple_bind_s(self._rootdn, self._rootpw)
        conn.modify_s('cn=foo,ou=users,dc=localhost', modlist)
        foo = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=foo)')
        self.assertEqual(foo[0][1]['mail'], [b'foo@email.com'])

    def test_modify_add(self):

        conn = self._makeOne()
        self._addUser('foo', mail=b'foo@bar.com')

        foo = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=foo)')
        old_values = foo[0][1]
        self.assertEqual(old_values['mail'], [b'foo@bar.com'])

        modlist = [(ldap.MOD_ADD, 'mail', [b'foo@email.com'])]
        conn.simple_bind_s(self._rootdn, self._rootpw)
        conn.modify_s('cn=foo,ou=users,dc=localhost', modlist)
        foo = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=foo)')
        self.assertEqual(set(foo[0][1]['mail']),
                         {b'foo@email.com', b'foo@bar.com'})

    def test_modrdn_wrongbase(self):
        conn = self._makeOne()
        conn.simple_bind_s(self._rootdn, self._rootpw)
        self.assertRaises(ldap.UNWILLING_TO_PERFORM,
                          conn.modrdn_s,
                          'cn=foo,o=base', 'cn=bar')

    def test_modrdn_wrongrecord(self):
        conn = self._makeOne()
        conn.simple_bind_s(self._rootdn, self._rootpw)
        self._addUser('foo')

        self.assertRaises(ldap.NO_SUCH_OBJECT, conn.modrdn_s,
                          'cn=bar,ou=users,dc=localhost', 'cn=baz')

    def test_modrdn_existing_clash(self):
        conn = self._makeOne()
        conn.simple_bind_s(self._rootdn, self._rootpw)
        self._addUser('foo')
        self._addUser('bar')

        self.assertRaises(ldap.ALREADY_EXISTS, conn.modrdn_s,
                          'cn=foo,ou=users,dc=localhost', 'cn=bar')

    def test_modrdn_success(self):
        conn = self._makeOne()
        conn.simple_bind_s(self._rootdn, self._rootpw)
        self._addUser('foo')

        foo = conn.search_s('cn=foo,ou=users,dc=localhost',
                            ldap.SCOPE_BASE,
                            filterstr='(objectClass=*)')
        self.assertTrue(foo)
        self.assertRaises(ldap.NO_SUCH_OBJECT, conn.search_s,
                          'cn=bar,ou=users,dc=localhost',
                          ldap.SCOPE_BASE,
                          filterstr='(objectClass=*)')

        conn.modrdn_s('cn=foo,ou=users,dc=localhost', 'cn=bar')
        self.assertRaises(ldap.NO_SUCH_OBJECT, conn.search_s,
                          'cn=foo,ou=users,dc=localhost',
                          ldap.SCOPE_BASE,
                          filterstr='(objectClass=*)')
        bar = conn.search_s('cn=bar,ou=users,dc=localhost',
                            ldap.SCOPE_BASE,
                            filterstr='(objectClass=*)')
        self.assertTrue(bar)


@unittest.skipIf(RealLDAPTests is object, 'LDAP server tests not available')
class RealLDAPModifyTests(FakeLDAPModifyTests, RealLDAPTests):
    pass
