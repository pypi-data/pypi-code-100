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
""" unit tests base classes
"""

import unittest

import ldap


class FakeLDAPTests(unittest.TestCase):

    _rootdn = 'cn=Manager,dc=localhost'
    _rootpw = 'TESTING'

    def setUp(self):
        from .. import TREE
        self.db = TREE
        self.db.addTreeItems('ou=users,dc=localhost')
        self.db.addTreeItems('ou=groups,dc=localhost')

    def tearDown(self):
        self.db.clear()

    def _getTargetClass(self):
        from .. import FakeLDAPConnection
        return FakeLDAPConnection

    def _makeOne(self, *args, **kw):
        conn = self._getTargetClass()(*args, **kw)
        return conn

    def _addUser(self, name, mail=None):
        from ..utils import hash_pwd

        if isinstance(name, str):
            encoded_name = name.encode('UTF-8')
        else:
            encoded_name = name

        conn = self._makeOne()
        user_dn = 'cn=%s,ou=users,dc=localhost' % name
        user_pwd = ('%s_secret' % name).encode('UTF-8')

        if conn.hash_password:
            pwd = hash_pwd(user_pwd)
        else:
            pwd = user_pwd

        user = [('cn', [encoded_name]),
                ('sn', [encoded_name]),
                ('userPassword', [pwd]),
                ('objectClass', [b'top', b'inetOrgPerson'])]
        if mail is not None:
            if isinstance(mail, str):
                mail = mail.encode('UTF-8')
            user.append(('mail', [mail]))

        conn.simple_bind_s(self._rootdn, self._rootpw)
        conn.add_s(user_dn, user)
        return (user_dn, user_pwd)

    def _addGroup(self, name, members=None):
        conn = self._makeOne()
        conn.simple_bind_s(self._rootdn, self._rootpw)
        group_dn = 'cn=%s,ou=groups,dc=localhost' % name

        if isinstance(name, str):
            encoded_name = name.encode('UTF-8')
        else:
            encoded_name = name

        group = [('cn', [encoded_name]), ('objectClass', [b'top', b'group'])]
        if members is not None:
            members = ['cn=%s,ou=users,dc=localhost' % x for x in members]
            group.append((conn.member_attr, members))

        conn.simple_bind_s(self._rootdn, self._rootpw)
        conn.add_s(group_dn, group)
        return group_dn


try:
    import volatildap

    # Try to run a server
    # safest test, there's too much that can go wrong.
    srv = volatildap.LdapServer()
    srv.start()
    srv.stop()

    class RealLDAPLayer:

        @classmethod
        def setUp(cls):
            schemas = ['core.schema', 'cosine.schema', 'inetorgperson.schema']
            cls._slapd = volatildap.LdapServer(
                            suffix='dc=localhost',
                            rootdn='cn=Manager,dc=localhost',
                            schemas=schemas)
            cls._slapd.start()

    class RealLDAPTests(FakeLDAPTests):

        layer = RealLDAPLayer

        def setUp(self):
            self._slapd = self.layer._slapd
            self._slapd.add(
                {'ou=users': {'ou': [b'users'],
                              'objectClass': [b'organizationalUnit']},
                 'ou=groups': {'ou': [b'groups'],
                               'objectClass': [b'organizationalUnit']}})

            self._rootdn = self._slapd.rootdn
            self._rootpw = self._slapd.rootpw

        def tearDown(self):
            self._slapd.reset()

        def _makeOne(self, *args, **kw):
            conn = ldap.initialize(self._slapd.uri)
            conn.hash_password = True
            conn.maintain_memberof = False
            conn.member_attr = 'member'
            conn.memberof_attr = 'memberOf'
            return conn

except (ImportError, SyntaxError, RuntimeError):
    RealLDAPTests = object
