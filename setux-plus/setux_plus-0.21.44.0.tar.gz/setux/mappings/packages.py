from setux.core.mapping import Packages


class Fedora(Packages):
    pkg = dict(
        netcat = 'nmap-ncat',
    )


class Arch(Packages):
    pkg = dict(
        netcat = 'openbsd-netcat',
        sqlite = 'sqlite3',
    )


class Fedora(Packages):
    pkg = dict(
        netcat = 'nmap-ncat',
    )


class Artix(Packages):
    pkg = dict(
        netcat = 'openbsd-netcat',
        sqlite = 'sqlite3',
        cron   = 'cronie',
    )
