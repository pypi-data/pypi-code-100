# Stuff
#

import grpc;

from mdb_bp import row
from mdb_bp.const import ERR_CONNECTION_CLOSED, ERR_QUERY_ACTIVE, ERR_CNFG_SUPPORT
from mdb_bp.protocol_buffers import odbc_pb2
from mdb_bp.protocol_buffers.odbc_pb2_grpc import MDBServiceStub
from mdb_bp.row import build_result_set
from mdb_bp.statement import stmt
from mdb_bp.result import result
from mdb_bp.transaction import tx, txOptions


class statusFlag:
    pass


class connection:
    def __init__(
            self,
            cfg,
    ):
        self.cfg = cfg
        # self.status = status

        self._channel = grpc.insecure_channel(self.cfg.get_address())
        self._stub    = MDBServiceStub(self._channel)

        self.closed = False

        # Query
        self.active_query  = False
        self._query_stream = None  # odbc_pb2_grpc.MDBServiceStub
        self._tx = None

        # Configure the connection
        self.auth = odbc_pb2.authPacket()

        initReq = odbc_pb2.InitializationRequest(
            username=self.cfg.username,
            password=self.cfg.password,
            db_name=self.cfg.database_name,
            auth=self.auth
        )

        self.auth = self._stub.InitializeConnection(initReq)

    def __enter__(self):
        return self

    def prepare(self, query):
        # Create and return a statement
        return stmt(self, query)

    # TODO @Paul: Finalize function
    def begin(self, isolation_level=1, read_only=False):
        # Make sure the db connection is still live
        if self.is_closed():
            raise Exception(ERR_CONNECTION_CLOSED)

        # Make sure this is the only tx?
        if self._tx is not None:
            raise Exception("concurrent transaction error")

        # Build the request
        req = odbc_pb2.XactRequest(
            auth=self.auth,
            isolation_level=isolation_level,
            read_only=read_only
        )

        resp = self._stub.Begin(req)

        self._tx = tx(
            conn=self,
            id=resp.xact_id,
            tx_options=txOptions(isolation_level, read_only)
        )
        return self._tx

    # TODO @Paul: Finalize function
    def exec(self, query, args=[]):
        # Make sure the db connection is still live
        if self.is_closed():
            raise Exception(ERR_CONNECTION_CLOSED)

        # Prepare the statement
        # Interpolate any parameters
        if len(args) != 0:
            if not self.cfg.parameters['interpolate_params']:
                raise Exception(ERR_CNFG_SUPPORT)

            query = self.cfg.interpolate_params(query, args)

        # Execute the query
        try:
            affected_rows, insert_id = self.exec_helper(query)
        except Exception as err:
            err = "Err: {}".format(err)
            print(err)
            raise Exception(err)

        # Generate the response
        return result(affected_rows, insert_id)

    def exec_helper(self, query):
        # Build the request object
        req = odbc_pb2.ExecRequest(
            auth=self.auth,
            statement=query
        )

        # Send the request using the connection stub
        resp = self._stub.Exec(req)
        # TODO: Update JWT

        # Generate the response
        return resp.affected_rows, resp.insert_id

    # TODO @Paul: Finalize function
    def query(self, query, args=[]):
        # Make sure the db connection is live
        if self.is_closed():
            raise Exception(ERR_CONNECTION_CLOSED)

        # Make sure there are no active queries
        if self.active_query:
            raise Exception(ERR_QUERY_ACTIVE)

        # Prepare the statement
        # Interpolate Parameters
        if len(args) != 0:
            if not self.cfg.parameters['interpolate_params']:
                raise Exception(ERR_CNFG_SUPPORT)

            query = self.cfg.interpolate_params(query, args)

        # Build the request
        req = odbc_pb2.QueryRequest(
            auth=self.auth,
            statement=query
        )

        # Execute the query
        try:
            resp_client = self._stub.Query(req)
            # TODO: Update JWT
        except Exception as err:
            err = "Err: {}".format(err)
            print(err)
            raise Exception(err)

        # # Update auth
        # self.auth = resp.auth

        # Store the query stream
        self._query_stream = resp_client

        rows = None
        for stream_resp in self._query_stream:
            if len(stream_resp.result_set) == 0:
                set = row.resultSet(row.build_column_list(stream_resp.resp_schema))
            else:
                set = build_result_set(stream_resp.resp_schema, stream_resp.result_set)

            rows = row.rows(
                stream_recv=self._query_stream,
                schema=stream_resp.resp_schema,
                set= set,
                done= stream_resp.done
            )
            break

        return rows

    def close(self):
        # Close the connection
        if not self.closed:
            self.closed = True

            # Close the gRPC channel
            if self._channel:
                self._channel.close()
            # Close the query stub
            # if self._query_stream:
            #     self._query_stream.close()

    def clear_tx(self):
        self._tx = None

    def is_closed(self):
        return self.closed
