
class tx:
    def __init__(self, conn, id, tx_options):
        self._conn    = conn
        self.id      = id
        self.options = tx_options

    def exec(self, query, args=[]):
        if not self._conn.is_closed():
            return self._conn.exec(query, args)
        raise Exception("Invalid connection")

    def query(self, query, args=[]):
        if not self._conn.is_closed():
            return self._conn.query(query, args)
        raise Exception("Invalid connection")

    def commit(self):
        if not self._conn.is_closed():
            resp = self._conn.exec("COMMIT")
            self.clear_tx()
            return resp
        raise Exception("Invalid connection")

    def rollback(self):
        if not self._conn.is_closed():
            resp = self._conn.exec("ROLLBACK")
            self.clear_tx()
            return resp
        raise Exception("Invalid connection")

    def clear_tx(self):
        self._conn.clear_tx()
        self._conn = None


class txOptions:
    def __init__(self, isolation_level, read_only):
        self.isolation = isolation_level
        self.read_only = read_only

