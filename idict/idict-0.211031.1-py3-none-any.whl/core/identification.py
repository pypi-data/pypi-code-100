#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the idict project.
#  Please respect the license - more about this in the section (*) below.
#
#  idict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  idict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with idict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and unethical regarding the effort and
#  time spent here.


import dis
from inspect import signature

from garoupa import Hosh, UT40_4
from ldict.exception import NoInputException
from orjson import dumps

from idict.core.compression import pack


def fhosh(f, version):
    """
    Create hosh with etype="ordered" using bytecodeof "f" as binary content.

    Usage:

    >>> print(fhosh(lambda x: {"z": x**2}, UT40_4))
    qowiXxlIUnfRg1ZyjR0trCb6-IUJBi6bgQpYHIM8

    Parameters
    ----------
    f
    version

    Returns
    -------

    """
    # Add signature.
    fargs = list(signature(f).parameters.keys())
    if not fargs:
        raise NoInputException(f"Missing function input parameters.")
    clean = [fargs]

    # Clean line numbers.
    groups = [l for l in dis.Bytecode(f).dis().split("\n\n") if l]
    for group in groups:
        lines = [segment for segment in group.split(" ") if segment][1:]
        clean.append(lines)

    return Hosh(dumps(clean), "ordered", version=version)


def key2id(key, digits):
    """
    >>> key2id("y", 40)
    'y-_0000000000000000000000000000000000000'

    >>> key2id("long bad field name", 40)
    'lo_6e6720626164206669656c64206e616d65000'

    >>> key2id("long bad field name that will be truncated", 40)
    'lo_6e6720626164206669656c64206e616d65207'

    Parameters
    ----------
    key

    Returns
    -------

    """
    prefix = key[:2].ljust(2, "-") + "_"
    rest = key[2:].encode().hex().ljust(digits - 3, "0")
    return prefix + rest[:digits - 3]


def removal_id(template, field):
    """
    >>> from garoupa import ø
    >>> removal_id(ø.delete, "myfield")
    '--------------------.............myfield'
    """
    return template[:-len(field)] + field


def blobs_hashes_hoshes(data, identity, ids):
    """
    >>> from idict import idict
    >>> idict(x=1, y=2, z=3, ids={"y": "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"}).show(colored=False)
    {
        "x": 1,
        "y": 2,
        "z": 3,
        "id": "Xkwes9zViTVf6Aj.LRFlhtrWYioyyyyyyyyyyyyy",
        "ids": {
            "x": "tY_a0e4015c066c1a73e43c6e7c4777abdeadb9f",
            "y": "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
            "z": "YB_957059a720926191bcc15ebde8f1b960282cd"
        }
    }
    """
    from idict.core.frozenidentifieddict import FrozenIdentifiedDict
    from idict.core.idict_ import Idict
    blobs = {}
    hashes = {}
    hoshes = {}
    for k, v in data.items():
        if k in ids:
            hoshes[k] = identity * ids[k]
        else:
            if isinstance(v, (Idict, FrozenIdentifiedDict)):
                hashes[k] = v.hosh
            else:
                blobs[k] = pack(v)
                hashes[k] = identity.h * blobs[k]
            hoshes[k] = hashes[k] ** key2id(k, identity.digits)
    return dict(blobs=blobs, hashes=hashes, hoshes=hoshes)
