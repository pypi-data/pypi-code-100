import asyncio
import os
import threading
from concurrent import futures
import pyarrow.parquet as pq
from bodo.io.fs_io import get_s3_bucket_region_njit


def get_parquet_filesnames_from_deltalake(delta_lake_path):
    try:
        from deltalake import DeltaTable
    except Exception as ywzb__kmjy:
        raise ImportError(
            "Bodo Error: please pip install the 'deltalake' package to read parquet from delta lake"
            )
    pofmy__tkb = None
    xqyl__fqknb = delta_lake_path.rstrip('/')
    psdfj__qdhgx = 'AWS_DEFAULT_REGION' in os.environ
    kyh__ikh = os.environ.get('AWS_DEFAULT_REGION', '')
    zqp__zbvzf = False
    if delta_lake_path.startswith('s3://'):
        rvnck__udtfc = get_s3_bucket_region_njit(delta_lake_path, parallel=
            False)
        if rvnck__udtfc != '':
            os.environ['AWS_DEFAULT_REGION'] = rvnck__udtfc
            zqp__zbvzf = True
    ocr__icy = DeltaTable(delta_lake_path)
    pofmy__tkb = ocr__icy.files()
    pofmy__tkb = [(xqyl__fqknb + '/' + odyab__rnkol) for odyab__rnkol in
        sorted(pofmy__tkb)]
    if zqp__zbvzf:
        if psdfj__qdhgx:
            os.environ['AWS_DEFAULT_REGION'] = kyh__ikh
        else:
            del os.environ['AWS_DEFAULT_REGION']
    return pofmy__tkb


def get_dataset_schema(dataset):
    if dataset.metadata is None and dataset.schema is None:
        if dataset.common_metadata is not None:
            dataset.schema = dataset.common_metadata.schema
        else:
            dataset.schema = dataset.pieces[0].get_metadata().schema
    elif dataset.schema is None:
        dataset.schema = dataset.metadata.schema
    vcly__mvlxs = dataset.schema.to_arrow_schema()
    if dataset.partitions is not None:
        for xfvp__zlfu in dataset.partitions.partition_names:
            if vcly__mvlxs.get_field_index(xfvp__zlfu) != -1:
                edk__eoxq = vcly__mvlxs.get_field_index(xfvp__zlfu)
                vcly__mvlxs = vcly__mvlxs.remove(edk__eoxq)
    return vcly__mvlxs


class VisitLevelThread(threading.Thread):

    def __init__(self, manifest):
        threading.Thread.__init__(self)
        self.manifest = manifest
        self.exc = None

    def run(self):
        try:
            manifest = self.manifest
            manifest.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(manifest.loop)
            manifest.loop.run_until_complete(manifest._visit_level(0,
                manifest.dirpath, []))
        except Exception as ywzb__kmjy:
            self.exc = ywzb__kmjy
        finally:
            if hasattr(manifest, 'loop') and not manifest.loop.is_closed():
                manifest.loop.close()

    def join(self):
        super(VisitLevelThread, self).join()
        if self.exc:
            raise self.exc


class ParquetManifest:

    def __init__(self, dirpath, open_file_func=None, filesystem=None,
        pathsep='/', partition_scheme='hive', metadata_nthreads=1):
        filesystem, dirpath = pq._get_filesystem_and_path(filesystem, dirpath)
        self.filesystem = filesystem
        self.open_file_func = open_file_func
        self.pathsep = pathsep
        self.dirpath = pq._stringify_path(dirpath)
        self.partition_scheme = partition_scheme
        self.partitions = pq.ParquetPartitions()
        self.pieces = []
        self._metadata_nthreads = metadata_nthreads
        self._thread_pool = futures.ThreadPoolExecutor(max_workers=
            metadata_nthreads)
        self.common_metadata_path = None
        self.metadata_path = None
        self.delta_lake_filter = set()
        yjdnc__gwvn = VisitLevelThread(self)
        yjdnc__gwvn.start()
        yjdnc__gwvn.join()
        self.pieces.sort(key=lambda piece: piece.path)
        if self.common_metadata_path is None:
            self.common_metadata_path = self.metadata_path
        self._thread_pool.shutdown()

    async def _visit_level(self, voqam__lwty, base_path, zjrp__qyl):
        fs = self.filesystem
        qhtar__llm, rxo__lgcdw, kywd__dvkd = await self.loop.run_in_executor(
            self._thread_pool, lambda fs, base_bath: next(fs.walk(base_path
            )), fs, base_path)
        if voqam__lwty == 0 and '_delta_log' in rxo__lgcdw:
            self.delta_lake_filter = set(get_parquet_filesnames_from_deltalake
                (base_path))
        vck__kjeyd = []
        for xqyl__fqknb in kywd__dvkd:
            if xqyl__fqknb == '':
                continue
            uxdrl__icj = self.pathsep.join((base_path, xqyl__fqknb))
            if xqyl__fqknb.endswith('_common_metadata'):
                self.common_metadata_path = uxdrl__icj
            elif xqyl__fqknb.endswith('_metadata'):
                self.metadata_path = uxdrl__icj
            elif self._should_silently_exclude(xqyl__fqknb):
                continue
            elif self.delta_lake_filter and uxdrl__icj not in self.delta_lake_filter:
                continue
            else:
                vck__kjeyd.append(uxdrl__icj)
        wbd__ezh = [self.pathsep.join((base_path, nsfxg__vjgf)) for
            nsfxg__vjgf in rxo__lgcdw if not pq._is_private_directory(
            nsfxg__vjgf)]
        vck__kjeyd.sort()
        wbd__ezh.sort()
        if len(vck__kjeyd) > 0 and len(wbd__ezh) > 0:
            raise ValueError('Found files in an intermediate directory: {}'
                .format(base_path))
        elif len(wbd__ezh) > 0:
            await self._visit_directories(voqam__lwty, wbd__ezh, zjrp__qyl)
        else:
            self._push_pieces(vck__kjeyd, zjrp__qyl)

    async def _visit_directories(self, voqam__lwty, rxo__lgcdw, zjrp__qyl):
        myz__wfih = []
        for xqyl__fqknb in rxo__lgcdw:
            axdew__yae, rjr__pkdl = pq._path_split(xqyl__fqknb, self.pathsep)
            agneg__kjqh, nke__pfzp = pq._parse_hive_partition(rjr__pkdl)
            vwrc__skif = self.partitions.get_index(voqam__lwty, agneg__kjqh,
                nke__pfzp)
            hlyb__pnny = zjrp__qyl + [(agneg__kjqh, vwrc__skif)]
            myz__wfih.append(self._visit_level(voqam__lwty + 1, xqyl__fqknb,
                hlyb__pnny))
        await asyncio.wait(myz__wfih)


ParquetManifest._should_silently_exclude = (pq.ParquetManifest.
    _should_silently_exclude)
ParquetManifest._parse_partition = pq.ParquetManifest._parse_partition
ParquetManifest._push_pieces = pq.ParquetManifest._push_pieces
pq.ParquetManifest = ParquetManifest


def pieces(self):
    return self._pieces


pq.ParquetDataset.pieces = property(pieces)


def partitions(self):
    return self._partitions


pq.ParquetDataset.partitions = property(partitions)
