class result:
    def __init__(self, affected_rows, insert_id):
        self.affected_rows = affected_rows
        self.insert_id = insert_id

    def __str__(self):
        resp = "{:<14} {:<14}\n".format("Affected Rows", "Insert ID")
        resp += "-------------- --------------\n"
        resp += "{:<14} {:<14}\n".format(self.affected_rows, self.insert_id)
        return resp

    def last_insert_id(self):
        return self.insert_id

    def rows_affected(self):
        return self.affected_rows
