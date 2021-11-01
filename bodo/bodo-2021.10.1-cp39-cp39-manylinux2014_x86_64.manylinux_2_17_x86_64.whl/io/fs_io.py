"""
S3 & Hadoop file system supports, and file system dependent calls
"""
import glob
import os
import warnings
from urllib.parse import urlparse
import llvmlite.binding as ll
import numba
import numpy as np
from numba.core import types
from numba.extending import overload
import bodo
from bodo.io import csv_cpp
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.str_ext import unicode_to_utf8, unicode_to_utf8_and_len
from bodo.utils.typing import BodoError, BodoWarning
from bodo.utils.utils import check_java_installation
_csv_write = types.ExternalFunction('csv_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.voidptr))
ll.add_symbol('csv_write', csv_cpp.csv_write)
bodo_error_msg = """
    Some possible causes:
        (1) Incorrect path: Specified file/directory doesn't exist or is unreachable.
        (2) Missing credentials: You haven't provided S3 credentials, neither through 
            environment variables, nor through a local AWS setup 
            that makes the credentials available at ~/.aws/credentials.
        (3) Incorrect credentials: Your S3 credentials are incorrect or do not have
            the correct permissions.
    """


def get_proxy_uri_from_env_vars():
    return os.environ.get('http_proxy', None) or os.environ.get('https_proxy',
        None) or os.environ.get('HTTP_PROXY', None) or os.environ.get(
        'HTTPS_PROXY', None)


def get_s3_fs(region=None, storage_options=None):
    from bodo.io.pyarrow_s3fs_fsspec_wrapper import PyArrowS3FS
    dtv__toxw = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    qxuoc__onip = False
    emwt__dwuu = get_proxy_uri_from_env_vars()
    if storage_options:
        qxuoc__onip = storage_options.get('anon', False)
    PyArrowS3FS.clear_instance_cache()
    fs = PyArrowS3FS(region=region, endpoint_override=dtv__toxw, anonymous=
        qxuoc__onip, proxy_options=emwt__dwuu)
    return fs


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.hdfs import HadoopFileSystem as HdFS
    uno__kpand = urlparse(path)
    if uno__kpand.scheme in ('abfs', 'abfss'):
        ulti__cfr = path
        if uno__kpand.port is None:
            nomb__rlbw = 0
        else:
            nomb__rlbw = uno__kpand.port
        zabd__cgc = None
    else:
        ulti__cfr = uno__kpand.hostname
        nomb__rlbw = uno__kpand.port
        zabd__cgc = uno__kpand.username
    try:
        fs = HdFS(host=ulti__cfr, port=nomb__rlbw, user=zabd__cgc)
    except Exception as dzgn__guhuf:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            dzgn__guhuf))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        wok__xwj = fs.isdir(path)
    except gcsfs.utils.HttpError as dzgn__guhuf:
        raise BodoError(
            f'{dzgn__guhuf}. Make sure your google cloud credentials are set!')
    return wok__xwj


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [ybgyq__vikgg.split('/')[-1] for ybgyq__vikgg in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        uno__kpand = urlparse(path)
        gzgjm__krx = (uno__kpand.netloc + uno__kpand.path).rstrip('/')
        dvf__rnm = fs.get_file_info(gzgjm__krx)
        if dvf__rnm.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if not dvf__rnm.size and dvf__rnm.type == pa_fs.FileType.Directory:
            return True
        return False
    except (FileNotFoundError, OSError) as dzgn__guhuf:
        raise
    except BodoError as fmrq__erqcn:
        raise
    except Exception as dzgn__guhuf:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(dzgn__guhuf).__name__}: {str(dzgn__guhuf)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    onb__rotz = None
    try:
        if s3_is_directory(fs, path):
            uno__kpand = urlparse(path)
            gzgjm__krx = (uno__kpand.netloc + uno__kpand.path).rstrip('/')
            dnj__umg = pa_fs.FileSelector(gzgjm__krx, recursive=False)
            nyu__vawpn = fs.get_file_info(dnj__umg)
            if nyu__vawpn and nyu__vawpn[0].path in [gzgjm__krx,
                f'{gzgjm__krx}/'] and int(nyu__vawpn[0].size or 0) == 0:
                nyu__vawpn = nyu__vawpn[1:]
            onb__rotz = [fhsk__vyyik.base_name for fhsk__vyyik in nyu__vawpn]
    except BodoError as fmrq__erqcn:
        raise
    except Exception as dzgn__guhuf:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(dzgn__guhuf).__name__}: {str(dzgn__guhuf)}
{bodo_error_msg}"""
            )
    return onb__rotz


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    uno__kpand = urlparse(path)
    puvx__vjpan = uno__kpand.path
    try:
        dxh__vmu = HadoopFileSystem.from_uri(path)
    except Exception as dzgn__guhuf:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            dzgn__guhuf))
    fashq__dfpu = dxh__vmu.get_file_info([puvx__vjpan])
    if fashq__dfpu[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not fashq__dfpu[0].size and fashq__dfpu[0].type == FileType.Directory:
        return dxh__vmu, True
    return dxh__vmu, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    onb__rotz = None
    dxh__vmu, wok__xwj = hdfs_is_directory(path)
    if wok__xwj:
        uno__kpand = urlparse(path)
        puvx__vjpan = uno__kpand.path
        dnj__umg = FileSelector(puvx__vjpan, recursive=True)
        try:
            nyu__vawpn = dxh__vmu.get_file_info(dnj__umg)
        except Exception as dzgn__guhuf:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(puvx__vjpan, dzgn__guhuf))
        onb__rotz = [fhsk__vyyik.base_name for fhsk__vyyik in nyu__vawpn]
    return dxh__vmu, onb__rotz


def abfs_is_directory(path):
    dxh__vmu = get_hdfs_fs(path)
    try:
        fashq__dfpu = dxh__vmu.info(path)
    except OSError as fmrq__erqcn:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if fashq__dfpu['size'] == 0 and fashq__dfpu['kind'].lower() == 'directory':
        return dxh__vmu, True
    return dxh__vmu, False


def abfs_list_dir_fnames(path):
    onb__rotz = None
    dxh__vmu, wok__xwj = abfs_is_directory(path)
    if wok__xwj:
        uno__kpand = urlparse(path)
        puvx__vjpan = uno__kpand.path
        try:
            vifcr__ictg = dxh__vmu.ls(puvx__vjpan)
        except Exception as dzgn__guhuf:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(puvx__vjpan, dzgn__guhuf))
        onb__rotz = [fname[fname.rindex('/') + 1:] for fname in vifcr__ictg]
    return dxh__vmu, onb__rotz


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype):
    from urllib.parse import urlparse
    kyuu__pialq = urlparse(path)
    fname = path
    fs = None
    mdpdh__dhpd = 'read_json' if ftype == 'json' else 'read_csv'
    dvwk__yilx = (
        f'pd.{mdpdh__dhpd}(): there is no {ftype} file in directory: {fname}')
    hfqiw__bzoo = directory_of_files_common_filter
    if kyuu__pialq.scheme == 's3':
        xlpgy__qvsjb = True
        fs = get_s3_fs_from_path(path)
        ijp__mjuj = s3_list_dir_fnames(fs, path)
        gzgjm__krx = (kyuu__pialq.netloc + kyuu__pialq.path).rstrip('/')
        fname = gzgjm__krx
        if ijp__mjuj:
            ijp__mjuj = [(gzgjm__krx + '/' + ybgyq__vikgg) for ybgyq__vikgg in
                sorted(filter(hfqiw__bzoo, ijp__mjuj))]
            cmh__tibe = [ybgyq__vikgg for ybgyq__vikgg in ijp__mjuj if int(
                fs.get_file_info(ybgyq__vikgg).size or 0) > 0]
            if len(cmh__tibe) == 0:
                raise BodoError(dvwk__yilx)
            fname = cmh__tibe[0]
        fvad__nxc = int(fs.get_file_info(fname).size or 0)
        lxwlo__tdolk = fs.open_input_file(fname)
    elif kyuu__pialq.scheme == 'hdfs':
        xlpgy__qvsjb = True
        fs, ijp__mjuj = hdfs_list_dir_fnames(path)
        fvad__nxc = fs.get_file_info([kyuu__pialq.path])[0].size
        if ijp__mjuj:
            path = path.rstrip('/')
            ijp__mjuj = [(path + '/' + ybgyq__vikgg) for ybgyq__vikgg in
                sorted(filter(hfqiw__bzoo, ijp__mjuj))]
            cmh__tibe = [ybgyq__vikgg for ybgyq__vikgg in ijp__mjuj if fs.
                get_file_info([urlparse(ybgyq__vikgg).path])[0].size > 0]
            if len(cmh__tibe) == 0:
                raise BodoError(dvwk__yilx)
            fname = cmh__tibe[0]
            fname = urlparse(fname).path
            fvad__nxc = fs.get_file_info([fname])[0].size
        lxwlo__tdolk = fs.open_input_file(fname)
    elif kyuu__pialq.scheme in ('abfs', 'abfss'):
        xlpgy__qvsjb = True
        fs, ijp__mjuj = abfs_list_dir_fnames(path)
        fvad__nxc = fs.info(fname)['size']
        if ijp__mjuj:
            path = path.rstrip('/')
            ijp__mjuj = [(path + '/' + ybgyq__vikgg) for ybgyq__vikgg in
                sorted(filter(hfqiw__bzoo, ijp__mjuj))]
            cmh__tibe = [ybgyq__vikgg for ybgyq__vikgg in ijp__mjuj if fs.
                info(ybgyq__vikgg)['size'] > 0]
            if len(cmh__tibe) == 0:
                raise BodoError(dvwk__yilx)
            fname = cmh__tibe[0]
            fvad__nxc = fs.info(fname)['size']
            fname = urlparse(fname).path
        lxwlo__tdolk = fs.open(fname, 'rb')
    else:
        if kyuu__pialq.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {kyuu__pialq.scheme}. Please refer to https://docs.bodo.ai/latest/source/file_io.html'
                )
        xlpgy__qvsjb = False
        if os.path.isdir(path):
            vifcr__ictg = filter(hfqiw__bzoo, glob.glob(os.path.join(path,
                '*')))
            cmh__tibe = [ybgyq__vikgg for ybgyq__vikgg in sorted(
                vifcr__ictg) if os.path.getsize(ybgyq__vikgg) > 0]
            if len(cmh__tibe) == 0:
                raise BodoError(dvwk__yilx)
            fname = cmh__tibe[0]
        fvad__nxc = os.path.getsize(fname)
        lxwlo__tdolk = fname
    return xlpgy__qvsjb, lxwlo__tdolk, fvad__nxc, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    fnjd__xlly = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            zlmc__txm, zyhy__kapeg = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = zlmc__txm.region
        except Exception as dzgn__guhuf:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{dzgn__guhuf}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = fnjd__xlly.bcast(bucket_loc)
    return bucket_loc


@numba.njit()
def get_s3_bucket_region_njit(s3_filepath, parallel):
    with numba.objmode(bucket_loc='unicode_type'):
        bucket_loc = ''
        if s3_filepath.startswith('s3://'):
            bucket_loc = get_s3_bucket_region(s3_filepath, parallel)
    return bucket_loc


def csv_write(path_or_buf, D, is_parallel=False):
    return None


@overload(csv_write, no_unliteral=True)
def csv_write_overload(path_or_buf, D, is_parallel=False):

    def impl(path_or_buf, D, is_parallel=False):
        txu__eadb = get_s3_bucket_region_njit(path_or_buf, parallel=is_parallel
            )
        bqeip__jub, qump__ldl = unicode_to_utf8_and_len(D)
        envd__ywu = 0
        if is_parallel:
            envd__ywu = bodo.libs.distributed_api.dist_exscan(qump__ldl, np
                .int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), bqeip__jub, envd__ywu,
            qump__ldl, is_parallel, unicode_to_utf8(txu__eadb))
        bodo.utils.utils.check_and_propagate_cpp_exception()
    return impl
