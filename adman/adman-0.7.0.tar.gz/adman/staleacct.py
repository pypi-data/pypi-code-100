from collections import defaultdict
from datetime import timedelta
from io import StringIO
import logging

from .adman import DISABLED_USER_FILTER
from .email import try_send_email
from .ldapfilter import Filter
from .util import count, datetime_to_FILETIME, utcnow

logger = logging.getLogger(__name__)

def lastlogon_before_filter(date):
    return Filter('lastLogonTimestamp<={}'.format(datetime_to_FILETIME(date)))


class StaleResult:
    def __init__(self, timestamp, user):
        self.timestamp = timestamp
        self.user = user        # user or computer

        # Can be:
        #   None (not cofigured to disable)
        #   True (disabled)
        #   Exception (failed to disable)
        self.disabled_status = None

    @property
    def name(self):
        return self.user.sAMAccountName

    @property
    def lastlogon(self):
        return self.user.lastLogonTimestamp.strftime('%Y-%m-%d %H:%M')

    @property
    def ago(self):
        return self.timestamp - self.user.lastLogonTimestamp


class FindStaleProcessor:
    def __init__(self):
        self.now = utcnow()
        self.results = defaultdict(dict)    # {what: {container: (cfg, [stale])}}

    def find(self, container, scope, getobj_meth, dt):
        # Identify the point in the past, before which the user must have logged on
        filt = lastlogon_before_filter(self.now - dt)
        filt &= ~DISABLED_USER_FILTER

        attrs = ('sAMAccountName', 'lastLogonTimestamp', 'userAccountControl')
        users = getobj_meth(rdn=container, scope=scope, filt=filt, attrs=attrs)

        results = []
        for user in users:
            sr = StaleResult(timestamp=self.now, user=user)
            assert sr.ago >= dt

            results.append(sr)

        return results


    def process(self, what, ucconfig, getobj_meth):
        total = 0
        for container, cfg in ucconfig.iterate_containers():
            stale = self.find(container=container, scope=cfg.scope,
                         getobj_meth=getobj_meth, dt=cfg.older_than.dt)
            if not stale:
                continue

            self.results[what][container] = (cfg, stale)
            total += len(stale)

            for sr in stale:
                if cfg.disable:
                    try:
                        sr.user.disabled = True
                        sr.user.commit()
                    # TODO: Tighten this up to include ldap.error and anything from .ldapobj
                    except Exception as e:
                        sr.disabled_status = e
                    else:
                        sr.disabled_status = True

        return total

    @property
    def disabled(self):
        for sr in self.flat_results():
            if sr.disabled_status is True:
                yield sr

    @property
    def disable_errors(self):
        for sr in self.flat_results():
            if isinstance(sr.disabled_status, Exception):
                yield sr, sr.disabled_status

    @property
    def total_stale(self):
        return count(self.flat_results())

    def flat_results(self):
        for what, containers in self.results.items():
            for container, (cfg, stale) in containers.items():
                for sr in stale:
                    yield sr


def _build_plaintext_report(fs, f):
    def _pr(*args, **kwargs):
        kwargs['file'] = f
        print(*args, **kwargs)

    _pr("ADMan Stale User report (generated {})".format(fs.now))
    _pr("-"*80)

    for what, containers in fs.results.items():
        _pr("\nStale {} accounts:".format(what))
        total = 0
        for container, (cfg, stale) in containers.items():
            _pr("  {} ({}) (>{} ago):".format(container, cfg.scope, cfg.older_than))
            total += len(stale)
            for sr in stale:
                line = "    {name:<24} {timestamp}  {ago:<15}".format(
                        name = sr.name,
                        timestamp = sr.lastlogon,
                        ago = '({} days ago)'.format(sr.ago.days),
                    )
                if sr.disabled_status:
                    st = 'DISABLED' if sr.disabled_status is True else 'failed to disable'
                    line += "  [{}]".format(st)
                _pr(line)
        if total:
            _pr("(Total: {})".format(total))


    # Add disable results
    if any(fs.disabled) or any(fs.disable_errors):
        _pr("\n" + "="*72)

    if any(fs.disabled):
        disabled = list(fs.disabled)
        _pr("\nDisabled ({}):".format(len(disabled)))
        for sr in disabled:
            _pr("  {}".format(sr.user.dn))

    if any(fs.disable_errors):
        _pr("\nErrors while disabling:")
        import traceback
        for sr, err in fs.disable_errors:
            _pr("  {}:".format(sr.user.dn))
            lines = traceback.format_exception(type(err), err, err.__traceback__)
            _pr("".join("    " + line for line in lines))



def find_and_process_stale_accounts(ad, config):
    sacfg = config.stale_accounts

    # Find and disable (if configured)
    fs = FindStaleProcessor()

    fs.process('user', sacfg.users, ad.get_users)
    fs.process('computer', sacfg.computers, ad.get_computers)

    if not any(fs.flat_results()):
        return

    buf = StringIO()
    _build_plaintext_report(fs, buf)

    if sacfg.email_to:
        subject = 'ADMan Stale User Report: {} stale'.format(fs.total_stale)
        ndis = count(fs.disabled)
        if ndis:
            subject += ', {} disabled'.format(ndis)
        ndiserr = count(fs.disable_errors)
        if ndiserr:
            subject += ', {} ERRORS'.format(ndiserr)

        try_send_email(config,
            mailto = sacfg.email_to,
            subject = subject,
            body = buf.getvalue(),
            )
    else:
        print(buf.getvalue())
