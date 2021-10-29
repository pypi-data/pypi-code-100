from types import MethodType

from xlwt import Utils
from xlwt import Worksheet
from xlwt import Workbook
from xlwt.compat import unicode_type

class mk_book(object):

    @staticmethod
    def insert_sheet(book: Workbook, sheet_name, cell_overwrite_ok=False, index=0):
        if hasattr(book, "insert_sheet"):
            pass
        else:
            book.insert_sheet = MethodType(mk_book.__insert, book)
        book.insert_sheet(sheet_name, cell_overwrite_ok, index)

    @staticmethod
    def __insert(self, sheet_name, cell_overwrite_ok=False, index=0):
        """
        This method is used to create Worksheets in a Workbook.
            :param sheetname:

              The name to use for this sheet, as it will appear in the
              tabs at the bottom of the Excel application.

            :param cell_overwrite_ok:

              If ``True``, cells in the added worksheet will not raise an
              exception if written to more than once.

            :return:

              The :class:`~xlwt.Worksheet.Worksheet` that was added.

            """
        if not isinstance(sheet_name, unicode_type):
            sheet_name = sheet_name.decode(self.encoding)
        if not Utils.valid_sheet_name(sheet_name):
            raise Exception("invalid worksheet name %r" % sheet_name)
        lower_name = sheet_name.lower()
        if lower_name in self._Workbook__worksheet_idx_from_name:
            raise Exception("duplicate worksheet name %r" % sheet_name)
        self._Workbook__worksheet_idx_from_name[lower_name] = len(self._Workbook__worksheets)
        self._Workbook__worksheets.insert(index, Worksheet(sheet_name, self, cell_overwrite_ok))
        return self._Workbook__worksheets[index]