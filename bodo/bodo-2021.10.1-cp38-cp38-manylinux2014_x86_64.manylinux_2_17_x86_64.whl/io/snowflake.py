from urllib.parse import parse_qsl, urlparse
import snowflake.connector
import bodo
from bodo.utils import tracing


def get_connection_params(conn_str):
    enay__fcp = urlparse(conn_str)
    yfyr__tcdsb = {}
    if enay__fcp.username:
        yfyr__tcdsb['user'] = enay__fcp.username
    if enay__fcp.password:
        yfyr__tcdsb['password'] = enay__fcp.password
    if enay__fcp.hostname:
        yfyr__tcdsb['account'] = enay__fcp.hostname
    if enay__fcp.port:
        yfyr__tcdsb['port'] = enay__fcp.port
    if enay__fcp.path:
        fkd__aect = enay__fcp.path
        if fkd__aect.startswith('/'):
            fkd__aect = fkd__aect[1:]
        rgur__rvwo, schema = fkd__aect.split('/')
        yfyr__tcdsb['database'] = rgur__rvwo
        if schema:
            yfyr__tcdsb['schema'] = schema
    if enay__fcp.query:
        for prpnc__ozr, yttmy__jylgp in parse_qsl(enay__fcp.query):
            yfyr__tcdsb[prpnc__ozr] = yttmy__jylgp
    return yfyr__tcdsb


class SnowflakeDataset(object):

    def __init__(self, batches, schema, conn):
        self.pieces = batches
        self._bodo_total_rows = 0
        for hfmq__yxg in batches:
            hfmq__yxg._bodo_num_rows = hfmq__yxg.rowcount
            self._bodo_total_rows += hfmq__yxg._bodo_num_rows
        self.schema = schema
        self.conn = conn


def get_dataset(query, conn_str):
    qzz__yxtn = tracing.Event('get_snowflake_dataset')
    from mpi4py import MPI
    yto__rcb = MPI.COMM_WORLD
    abk__ilbjm = tracing.Event('snowflake_connect', is_parallel=False)
    rmuci__ejvl = get_connection_params(conn_str)
    conn = snowflake.connector.connect(**rmuci__ejvl)
    abk__ilbjm.finalize()
    if bodo.get_rank() == 0:
        pog__njf = conn.cursor()
        fevc__oso = tracing.Event('get_schema', is_parallel=False)
        bzpl__liz = f'select * from ({query}) x LIMIT {100}'
        schema = pog__njf.execute(bzpl__liz).fetch_arrow_all().schema
        fevc__oso.finalize()
        ejrj__oehz = tracing.Event('execute_query', is_parallel=False)
        pog__njf.execute(query)
        ejrj__oehz.finalize()
        batches = pog__njf.get_result_batches()
        yto__rcb.bcast((batches, schema))
    else:
        batches, schema = yto__rcb.bcast(None)
    geghu__ltbf = SnowflakeDataset(batches, schema, conn)
    qzz__yxtn.finalize()
    return geghu__ltbf
