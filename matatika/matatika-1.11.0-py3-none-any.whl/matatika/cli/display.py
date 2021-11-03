"""CLI display module"""

import click


class Column:
    """Class to handle a table column"""

    def __init__(self, heading: str = None):

        heading = heading and str(heading)

        self._heading = heading
        self._data = []

    def __iter__(self):
        column = self._data

        if self.heading:
            column.insert(0, self.heading)

        for value in column:
            yield value

    def __getitem__(self, i: int):
        return self._data[i]

    @property
    def heading(self) -> str:
        """Gets the column heading"""

        return self._heading

    @heading.setter
    def heading(self, heading: str):

        self._heading = heading and str(heading)

    def add(self, *values):
        """Adds one or more values to the column"""

        for value in values:
            self._data.append(value and str(value))


class Table:
    """Class to handle a command-line table"""

    def __init__(self, *cols):
        self.cols = cols

    def __repr__(self):
        return self.create()

    def create(self, separator: str = "\t", max_cell_size: int = 64) -> str:
        """Creates the table as a string"""

        modified_cols = []

        for col in self.cols:

            modified_col = []

            # convert values to str
            for element in col:
                modified_col.append(str(element))

            # find the largest cell, then constrain and update largest cell if necessary
            largest_cell = max(modified_col, key=len)

            if len(largest_cell) > max_cell_size:
                truncated_val = largest_cell[:max_cell_size - 1] + "\u2026"
                modified_col[modified_col.index(largest_cell)] = truncated_val
                largest_cell = truncated_val

            # right-pad all column cells to thd size of the largest cell
            for i, cell in enumerate(modified_col):
                if len(cell) > max_cell_size:
                    cell = cell[:max_cell_size - 1] + "\u2026"

                modified_col[i] = cell.ljust(len(largest_cell))

                if cell == str(None):
                    modified_col[i] = click.style(modified_col[i], fg='yellow')

            modified_cols.append(modified_col)

        rows = []

        # construct each row
        for i, _ in enumerate(modified_cols[0]):
            rows.append(separator.join([col[i] for col in modified_cols]))

        return "\n".join(rows)
