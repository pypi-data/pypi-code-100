from re import compile

from setux.core.module import Module
from setux.logger import debug


class Distro(Module):
    '''Update Config File (sed)
    '''
    def deploy(self, target, *, cfg, src=None, dst):
        cont = target.read(cfg, report='quiet')
        if dst in cont: return True
        msg = [f'{cfg} <>']
        if src:
            sre = compile(src).search
            updated, found = [], False
            for line in cont.split('\n'):
                if sre(line):
                    found = True
                    msg.append(f' <  {line}')
                    msg.append(f'  > {dst}')
                    updated.append(dst)
                else:
                    updated.append(line)
            if not found:
                updated.append(dst)
            target.write(cfg, '\n'.join(updated)+'\n', report='quiet')
        else:
            msg.append(f'  > {dst}')
            target.write(cfg, f'{cont}{dst}\n', report='quiet')

        debug('\n'.join(msg))
        return True
