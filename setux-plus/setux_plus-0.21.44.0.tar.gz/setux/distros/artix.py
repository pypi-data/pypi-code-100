from setux.core.distro import Distro


class Artix(Distro):
    Package = 'pacman'
    Service = 'runit'
    etcsvdir = '/etc/runit/sv'
    runsvdir = '/run/runit/service'
    pkgmap = dict(
        pip        = 'python-pip',
        setuptools = 'python-setuptools',
    )
    svcmap = dict(
        ssh  = 'sshd',
    )

    @classmethod
    def release_name(cls, infos):
        return infos['DISTRIB_ID']
