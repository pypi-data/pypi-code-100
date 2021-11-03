from setux.core.distro import Distro


class Fedora(Distro):
    Package = 'dnf'
    Service = 'SystemD'
    pkgmap = dict(
        pip        = 'python3-pip',
        setuptools = 'python3-setuptools',
    )
    svcmap = dict(
        ssh = 'sshd',
    )
    @classmethod
    def release_name(cls, infos):
        did = infos['ID'].strip()
        ver = infos['VERSION_ID']
        return f'{did}_{ver}'


class fedora_30(Fedora): pass

class fedora_32(Fedora): pass

class fedora_34(Fedora): pass


