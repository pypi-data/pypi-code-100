from setux.core.module import Module


class Distro(Module):
    '''Minimum System Requieremnts
    '''
    def do_deploy(self, target, **kw):
        return self.install(target,
            pkg = 'tmux vim',
        )


class FreeBSD(Distro):
    def do_deploy(self, target, **kw):
        return self.install(target,
            pkg = 'sudo bash python',
        )

