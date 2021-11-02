##############################################################################
#
# Copyright (c) 2012-2021 Jens Vagelpohl and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import functools
import inspect
from base64 import b64encode
from hashlib import sha1 as sha_new

import ldap.dn


def check_types(*tested):
    """ Decorator to check parameter types """

    def _check_types(called_function):
        spec = inspect.getfullargspec(called_function)
        test_indices = [(name, typ, spec[0].index(name))
                        for (name, typ) in tested
                        if name in spec[0]]

        @functools.wraps(called_function)
        def _check(*args, **kw):
            for arg_name, arg_type, arg_index in test_indices:
                if arg_name in kw:
                    arg_val = kw.get(arg_name)
                elif arg_index < len(args):
                    arg_val = args[arg_index]
                else:
                    continue  # fallback to default arguments

                if not isinstance(arg_val, arg_type):
                    msg = 'Parameter "%s" must be %s, found %s (%s)'
                    raise TypeError(msg % (arg_name,
                                           arg_type.__name__,
                                           str(arg_val),
                                           type(arg_val).__name__))

            return called_function(*args, **kw)

        return _check

    return _check_types


def hash_pwd(pwd_str):
    if isinstance(pwd_str, str):
        pwd_str = pwd_str.encode('utf-8')
    sha_digest = sha_new(pwd_str).digest()
    return b'{SHA}%s' % b64encode(sha_digest).strip()


@check_types(('dn', str),)
def explode_dn(dn):
    parts = []
    raw_parts = ldap.dn.explode_dn(dn)
    for part in raw_parts:
        parts.append(part)

    return parts


def to_utf8(to_convert):
    if not isinstance(to_convert, bytes):
        to_convert = to_convert.encode('UTF-8')
    return to_convert


def from_utf8(to_convert):
    if isinstance(to_convert, bytes):
        to_convert = to_convert.decode('UTF-8')
    return to_convert
