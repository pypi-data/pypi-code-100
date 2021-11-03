from ._utils import Command

__all__ = [
    'admin_bucket_remote_add',
    'admin_bucket_remote_edit',
    'admin_bucket_remote_ls',
    'admin_bucket_remote_rm',
    'admin_bucket_quota_fifo',
    'admin_bucket_quota_hard',
]

BUCKET_REMOTE_COMMAND = 'mc {flags} admin bucket remote'




def admin_bucket_remote_add(**kwargs):
    '''Add new remote target.

    Usage::

      >>> r = admin_bucket_remote_add(target='aliasforhost', endpoint='http(s)://ACCESSKEY:SECRETKEY@DEST_URL/DEST_BUCKET')
      >>> r.content
      {'status': 'success', 'policy': 'admins', 'isGroup': False}
    '''
    cmd = Command(BUCKET_REMOTE_COMMAND + ' add {target} {endpoint}')
    raise Exception(cmd.command)
    return cmd(**kwargs)