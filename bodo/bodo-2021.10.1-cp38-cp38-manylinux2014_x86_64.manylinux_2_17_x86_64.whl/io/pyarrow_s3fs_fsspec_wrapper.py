from urllib.parse import urlparse
import pyarrow.fs as pa_fs
from fsspec import AbstractFileSystem
from pyarrow.fs import S3FileSystem


class PyArrowS3FS(AbstractFileSystem):
    protocol = 's3'

    def __init__(self, *, access_key=None, secret_key=None, session_token=
        None, anonymous=False, region=None, scheme=None, endpoint_override=
        None, background_writes=True, role_arn=None, session_name=None,
        external_id=None, load_frequency=900, proxy_options=None, **kwargs):
        super().__init__(self, **kwargs)
        self.pa_s3fs = S3FileSystem(access_key=access_key, secret_key=
            secret_key, session_token=session_token, anonymous=anonymous,
            region=region, scheme=scheme, endpoint_override=
            endpoint_override, background_writes=background_writes,
            role_arn=role_arn, session_name=session_name, external_id=
            external_id, load_frequency=load_frequency, proxy_options=
            proxy_options)

    def __getattribute__(self, name: str):
        if name == '__class__':
            return PyArrowS3FS
        if name in ['__init__', '__getattribute__', '_open', 'open', 'ls',
            'isdir', 'isfile']:
            return lambda *args, **kw: getattr(PyArrowS3FS, name)(self, *
                args, **kw)
        lyuzq__hjshk = object.__getattribute__(self, '__dict__')
        mgk__pzsg = lyuzq__hjshk.get('pa_s3fs', None)
        if name == 'pa_s3fs':
            return mgk__pzsg
        if mgk__pzsg is not None and hasattr(mgk__pzsg, name):
            return getattr(mgk__pzsg, name)
        return super().__getattribute__(name)

    def _open(self, path, mode='rb', block_size=None, autocommit=True,
        cache_options=None, **kwargs):
        ycw__lbs = urlparse(path)
        euhu__bvjf = ycw__lbs.netloc + ycw__lbs.path
        return self.pa_s3fs.open_input_file(euhu__bvjf)

    def ls(self, path, detail=True, **kwargs):
        ycw__lbs = urlparse(path)
        euhu__bvjf = (ycw__lbs.netloc + ycw__lbs.path).rstrip('/')
        gmn__abko = pa_fs.FileSelector(euhu__bvjf, recursive=False)
        tqpq__aqhq = self.pa_s3fs.get_file_info(gmn__abko)
        if len(tqpq__aqhq) == 0:
            if self.isfile(path):
                if detail:
                    return [{'type': 'file', 'name': euhu__bvjf}]
                else:
                    return [euhu__bvjf]
            return []
        if tqpq__aqhq and tqpq__aqhq[0].path in [euhu__bvjf, f'{euhu__bvjf}/'
            ] and int(tqpq__aqhq[0].size or 0) == 0:
            tqpq__aqhq = tqpq__aqhq[1:]
        ckg__bgx = []
        if detail:
            for ltyt__ymr in tqpq__aqhq:
                yvux__ylznt = {}
                if ltyt__ymr.type == pa_fs.FileType.Directory:
                    yvux__ylznt['type'] = 'directory'
                elif ltyt__ymr.type == pa_fs.FileType.File:
                    yvux__ylznt['type'] = 'file'
                else:
                    yvux__ylznt['type'] = 'unknown'
                yvux__ylznt['name'] = ltyt__ymr.base_name
                ckg__bgx.append(yvux__ylznt)
        else:
            ckg__bgx = [ltyt__ymr.base_name for ltyt__ymr in tqpq__aqhq]
        return ckg__bgx

    def isdir(self, path):
        ycw__lbs = urlparse(path)
        euhu__bvjf = (ycw__lbs.netloc + ycw__lbs.path).rstrip('/')
        qjkd__obdu = self.pa_s3fs.get_file_info(euhu__bvjf)
        return (not qjkd__obdu.size and qjkd__obdu.type == pa_fs.FileType.
            Directory)

    def isfile(self, path):
        ycw__lbs = urlparse(path)
        euhu__bvjf = (ycw__lbs.netloc + ycw__lbs.path).rstrip('/')
        qjkd__obdu = self.pa_s3fs.get_file_info(euhu__bvjf)
        return qjkd__obdu.type == pa_fs.FileType.File
