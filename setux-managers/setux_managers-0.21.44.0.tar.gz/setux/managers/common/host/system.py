from pybrary.net import get_ip_adr
from pybrary.func import memo

from setux.core.manage import Manager
from setux.logger import logger, error, info


class Distro(Manager):
    '''System Infos
    '''
    manager = 'system'

    @property
    def hostname(self):
        attr = '_hostname_'
        try:
            val = getattr(self, attr)
        except AttributeError:
            ret, out, err = self.run('hostname')
            val = out[0]
            setattr(self, attr,  val)
        return val

    @hostname.setter
    def hostname(self, val):
        attr = '_hostname_'
        delattr(self, attr)
        new_val = val.replace('_', '-')

        try:
            with logger.quiet():
                new_hostname = self.target.read('/etc/hostname')
                current = new_hostname.strip()
                if current==new_val: return
                new_hostname = new_hostname.replace(current, new_val)
                ok = self.target.write('/etc/hostname', new_hostname)
                if not ok: raise RuntimeError('Error writing hostname')

                new_hosts = self.target.read('/etc/hosts')
                new_hosts = new_hosts.replace(current, new_val)
                ok = self.target.write('/etc/hosts', new_hosts)
                if not ok: raise RuntimeError('Error writing hosts')

                ret, out, err = self.run(f'hostname {new_val}')
                ok = ret==0
                if not ok: raise RuntimeError('Error setting hostname')
        except Exception as x:
            error(f'hostname -> {new_val} ! {x}')
            return False

        info(f'hostname -> {new_val} .')
        return True

    @memo
    def fqdn(self):
        ret, out, err = self.run('hostname -f')
        return out[0]
