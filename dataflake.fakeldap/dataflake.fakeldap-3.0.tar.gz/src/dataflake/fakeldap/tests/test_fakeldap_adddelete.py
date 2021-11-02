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

    def test_add_wrongbase(self):
        conn = self._makeOne()
        foo2 = [('cn', [b'foo']),
                ('sn', [b'foo']),
                ('userPassword', [b'somepass']),
                ('objectClass', [b'top', b'inetOrgPerson'])]
        self.assertRaises(ldap.UNWILLING_TO_PERFORM, conn.add_s,
                          'cn=foo,o=base', foo2)

    def test_add_existing_clash(self):
        conn = self._makeOne()
        conn.simple_bind_s(self._rootdn, self._rootpw)
        self._addUser('foo')

        foo2 = [('cn', [b'foo']),
                ('sn', [b'foo']),
                ('userPassword', [b'somepass']),
                ('objectClass', [b'top', b'inetOrgPerson'])]
        self.assertRaises(ldap.ALREADY_EXISTS, conn.add_s,
                          'cn=foo,ou=users,dc=localhost', foo2)

    def test_add_success(self):
        import copy
        from ldap.modlist import addModlist
        conn = self._makeOne()
        conn.simple_bind_s(self._rootdn, self._rootpw)
        self._addUser('foo')

        foo = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=foo)')
        bar_values = copy.deepcopy(foo[0][1])
        bar_values['cn'] = [b'bar']
        modlist = addModlist(bar_values)

        self.assertFalse(conn.search_s('ou=users,dc=localhost',
                                       ldap.SCOPE_SUBTREE,
                                       filterstr='(cn=bar)'))
        conn.add_s('cn=bar,ou=users,dc=localhost', modlist)
        self.assertTrue(conn.search_s('ou=users,dc=localhost',
                                      ldap.SCOPE_SUBTREE,
                                      filterstr='(cn=bar)'))

    def test_delete_wrongbase(self):
        conn = self._makeOne()
        self.assertRaises(ldap.UNWILLING_TO_PERFORM,
                          conn.delete_s,
                          'cn=foo,o=base')

    def test_modrdn_wrongrecord(self):
        conn = self._makeOne()
        conn.simple_bind_s(self._rootdn, self._rootpw)
        self._addUser('foo')

        self.assertRaises(ldap.NO_SUCH_OBJECT, conn.delete_s,
                          'cn=bar,ou=users,dc=localhost')

    def test_delete_success(self):
        conn = self._makeOne()
        conn.simple_bind_s(self._rootdn, self._rootpw)
        self._addUser('foo')

        foo = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=foo)')
        self.assertTrue(foo)
        conn.delete_s('cn=foo,ou=users,dc=localhost')
        foo = conn.search_s('ou=users,dc=localhost',
                            ldap.SCOPE_SUBTREE,
                            filterstr='(cn=foo)')
        self.assertFalse(foo)


@unittest.skipIf(RealLDAPTests is object, 'LDAP server tests not available')
class RealLDAPModifyTests(FakeLDAPModifyTests, RealLDAPTests):
    pass
