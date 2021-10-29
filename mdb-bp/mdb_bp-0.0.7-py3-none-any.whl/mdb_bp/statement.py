
class stmt:
    def __init__(self, conn, query):
        self.conn        = conn
        self.stmt        = query
        self.param_count = query.count("?")

    def close(self):
        if not self.conn.is_closed():
            self.conn.close()

    def num_input(self):
        return self.param_count

    def exec(self, args=[]):
        return self.conn.exec(self.stmt, args)

    def query(self, args):
        return self.conn.query(self.stmt, args)
