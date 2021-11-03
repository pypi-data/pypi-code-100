from setux.core.service import Service


class Distro(Service):
    '''RUNIT Services managment
    '''
    manager = 'runit'

    def do_enabled(self, svc):
        ret, out, err = self.run(
            f'ls {self.distro.runsvdir}/{svc}'
        )
        out = out and out[0] or ''
        return 'supervise' in out

    def do_status(self, svc):
        ret, out, err = self.run(
            f'sv status {svc}',
        )
        out = out and out[0] or ''
        return out.startswith('run')

    def do_start(self, svc):
        self.run(
            f'sv up {svc}'
        )

    def do_stop(self, svc):
        self.run(
            f'sv down {svc}'
        )

    def do_restart(self, svc):
        self.run(
            f'sv restart {svc}'
        )

    def do_enable(self, svc):
        self.run(
            f'ln -s {self.distro.etcsvdir}/{svc} {self.distro.runsvdir}/'
        )

    def do_disable(self, svc):
        self.run(
            f'unlink {self.distro.runsvdir}/{svc}'
        )
