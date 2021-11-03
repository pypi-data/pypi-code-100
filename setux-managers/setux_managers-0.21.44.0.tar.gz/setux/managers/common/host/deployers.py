from setux.core.deploy import Deployer


class hostanme(Deployer):
    @property
    def label(self):
        return 'hostname'

    def check(self):
        ret, out, err = self.target.run(f'hostname')
        return out[0] == self.name

    def deploy(self):
        ret, out, err = self.target.run(f'hostname {self.name}')
        return ret == 0


class etc_hostanme(Deployer):
    @property
    def label(self):
        return '/etc/hostname'

    def check(self):
        current = self.target.read('/etc/hostname').strip()
        return current == self.name

    def deploy(self):
        ok = self.target.write(
            '/etc/hostname',
            f'{self.name}\n',
        )
        return ok


class etc_hosts(Deployer):
    @property
    def label(self):
        return '/etc/hosts'

    def check(self):
        current = self.target.read('/etc/hosts')
        return self.name in current

    def deploy(self):
        current =  self.target.read('/etc/hostname').strip()
        new_hosts = self.target.read('/etc/hosts')
        new_hosts = new_hosts.replace(current, self.name)
        ok = self.target.write('/etc/hosts', new_hosts)
        return ok


class Hostname(Deployer):
    @property
    def label(self):
        return f'hostname {self.name}'

    def check(self):
        ok = hostanme(target=self.target, name=self.name).check()
        if not ok: return False
        ok = etc_hostanme(target=self.target, name=self.name).check()
        if not ok: return False
        ok = etc_hosts(target=self.target, name=self.name).check()
        if not ok: return False
        return True

    def deploy(self):
        ok = etc_hosts(target=self.target, name=self.name)()
        if not ok: return False
        ok = etc_hostanme(target=self.target, name=self.name)()
        if not ok: return False
        ok = hostanme(target=self.target, name=self.name)()
        if not ok: return False
        return True

