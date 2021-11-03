from setux.core.service import Service


class Distro(Service):
    '''SystemV Services management
    '''
    manager = 'SystemV'

    def do_enabled(self, svc):
        rc = f'/etc/rc3.d/S03{svc}'
        ret, out, err = self.run('ls', rc)
        return out[0]==rc

    def do_status(self, svc):
        ret, out, err = self.run(
            f'service {svc} status',
        )
        return 'is running' in out[0] if out else False

    def do_start(self, svc):
        self.run(f'service {svc} start')

    def do_stop(self, svc):
        self.run(f'service {svc} stop')

    def do_restart(self, svc):
        self.run(f'service {svc} restart')

    def do_enable(self, svc):
        self.run(f'update-rc.d {svc} enable')

    def do_disable(self, svc):
        self.run(f'update-rc.d {svc} disable')
