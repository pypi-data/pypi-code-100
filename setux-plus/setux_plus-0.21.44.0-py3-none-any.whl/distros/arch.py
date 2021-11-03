from setux.core.distro import Distro


class Arch(Distro):
    Package = 'pacman'
    Service = 'SystemD'
    pkgmap = dict(
        pip        = 'python-pip',
        setuptools = 'python-setuptools',
    )
    svcmap = dict(
        ssh = 'sshd',
    )
