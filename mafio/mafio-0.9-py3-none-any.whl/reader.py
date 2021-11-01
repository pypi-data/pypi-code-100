import gzip


class MAFReader:
    def __init__(self, path, compression=None):
        """Reader instance responsible for reading the file.

        Args:
            path (): Path to file to read from.
            compression (string, optional): Compression of file.
            Currently supports gzip. Defaults to None.
        """
        self.path = path
        self._parsers = {
            "gzip": gzip.open,
            "native": open
        }
        self.headers = None
        if compression:
            self._parser = self._parsers[compression]
        else:
            self._parser = self._parsers["native"]

    def read(self, chunk_size=None, use_cols=None):
        """Read MAF file data into a list containing the values

        Args:
            chunk_size (int, optional): Read the file in chunks.
            Useful with very large datasets. Defaults to None.
            use_cols (list, optional): Extract only values corresponding to the
            list of columns given. Defaults to None.
            Defaults to False.

        Yields:
            list: list of rows
        """
        with self._parser(self.path, "rb") as file:
            if chunk_size:
                yield from self.__read_chunks(file, chunk_size, use_cols)
            else:
                yield from self.__read_bulk(file, use_cols)

    def __read_bulk(self, file, use_cols=None):

        if use_cols:
            rows = []
            for i,row in enumerate(file.readlines()):
                row = self.__format_row(row)
                
                # get column names
                if i == 0:
                    self.headers = row
                
                # pick desired columns
                indices = [self.headers.index(col) for col in use_cols]
                rows.append([row[index] for index in indices])
        else:
            rows = [self.__format_row(row) for row in file.readlines()]

        yield rows

    def __read_chunks(self, file, chunk_size=1024, use_cols=None):

        if use_cols:
            self.headers = self.__format_row(file.readline())
            indices = [self.headers.index(col) for col in use_cols]
        else:
            indices = None

        while True:
            rows = []
            for _ in range(chunk_size):
                row = file.readline()
                if row:
                    row = self.__format_row(row)
                    if indices:
                        rows.append([row[index] for index in indices])
                    else:
                        rows.append(row)
                # End of file
                else:
                    if len(rows) == 0:
                        return
                    yield rows
                    return
            yield rows

    def __format_row(self, row):
        row = row.decode().split("\t")
        row[-1] = row[-1].rstrip("\r\n")
        return row
