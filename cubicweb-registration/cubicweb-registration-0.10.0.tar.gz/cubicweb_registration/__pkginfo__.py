# pylint: disable-msg=W0622
"""cubicweb-registration application packaging information"""

modname = "registration"
distname = "cubicweb-registration"

numversion = (0, 10, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
description = "public registration component for the CubicWeb framework"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/%s" % distname
classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: JavaScript",
]

__depends__ = {
    "cubicweb": ">= 3.27.0, < 3.34.0",
    "cubicweb-forgotpwd": None,
    "Pillow": None,
}
