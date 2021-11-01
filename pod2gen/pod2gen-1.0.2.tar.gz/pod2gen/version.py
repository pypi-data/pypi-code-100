# -*- coding: utf-8 -*-
"""
    pod2gen.version
    ~~~~~~~~~~~~~~~

    :copyright: 2013, Lars Kiesow <lkiesow@uos.de>; 2016, Thorben Dahl
        <thorben@sjostrom.no>; 2021, Slim Beji <mslimbeji@gmail.com>

    :license: FreeBSD and LGPL, see license.* for more details.

"""
"Version of pod2gen represented as tuple"
version = (1, 0, 2)


"Version of pod2gen represented as string"
version_str = ".".join([str(x) for x in version])

version_major = version[:1]
version_minor = version[:2]
version_full = version

version_major_str = ".".join([str(x) for x in version_major])
version_minor_str = ".".join([str(x) for x in version_minor])
version_full_str = ".".join([str(x) for x in version_full])

"Name of this project"
name = "pod2gen"

"Website of this project"
website = "https://pod2gen.caproni.fm"
