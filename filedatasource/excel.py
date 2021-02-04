from abc import ABC, ABCMeta
from typing import Union, List

from filedatasource.datafile import DataReader, DataFile, DataWriter, ReadMode


class ExcelData(DataFile, ABC):
    """ Abstract class to define the common attributes of the Excel files. """
    __metaclass__ = ABCMeta

    @property
    def fieldnames(self) -> List[str]:
        """
        :return: The list of fieldnames.
        """
        return self._fieldnames

    @property
    def sheet_name(self) -> str:
        """
        :return:  The sheet name.
        """
        return self.__sheet_name

    @property
    def sheet(self):
        """
        :return: The sheet object.
        """
        return self._sheet

    def __init__(self, fname: str, sheet: Union[str, int] = None) -> None:
        """ Constructor.
        :param fname: The file path to the Excel file.
        :param sheet: The sheet to read/write.
        """
        super().__init__(fname)
        self.__sheet_name = sheet if sheet else 0
        self._sheet = None
        self._fieldnames = []


class ExcelReader(ExcelData, DataReader):
    """ The class to read an Excel file easily. """
    def __init__(self, fname: str, sheet: Union[str, int] = None, mode: ReadMode = ReadMode.OBJECT) -> None:
        """ Constructor.
        :param fname: The file path to the Excel file.
        :param sheet: The sheet to read/write.
        :param mode: The default mode to read the rows.
        """
        super(ExcelReader, self).__init__(fname, sheet=sheet)
        DataReader.__init__(self, fname, mode=mode)
        try:
            xlrd = __import__('xlrd')
        except ImportError:
            raise ModuleNotFoundError('xlrd is required. Please, install it with:\n\npip install xlrd')
        doc = xlrd.open_workbook(fname)
        self.__doc = doc
        sheet = 0 if sheet is None else sheet
        self._sheet = doc.sheet_by_name(sheet) if isinstance(sheet, str) else doc.sheet_by_index(sheet)
        self.__row = 0
        self._fieldnames = [cell.value for cell in self.sheet.row(self.__row)]

    def read_row(self) -> object:
        """ Read a row of the Excel file as a dict.

        :return: A dictionary where the keys are the fieldnames, and their values the row values.
        """
        if self.__row < self.sheet.nrows - 1:
            self.__row += 1
            row = self.sheet.row(self.__row)
            return {self.fieldnames[i]: cell.value for i, cell in enumerate(row)}
        raise StopIteration()

    def close(self) -> None:
        """ Nothing to do. """
        pass

    def __len__(self) -> int:
        """
        :return: The number of rows.
        """
        return self.sheet.nrows - 1



class ExcelWriter(ExcelData, DataWriter):

    def __init__(self, fname: str, sheet: Union[str, int] = None, fieldnames: Union[List[str], type, object] = None,):
        super().__init__(fname, sheet)
        self._fieldnames = self._parse_fieldnames(fieldnames)
        try:
            xlwt = __import__('xlwt')
        except ImportError:
            raise ModuleNotFoundError('xlwt is required. Please, install it with:\n\npip install xlwt')
        self._doc = xlwt.Workbook()
        self._sheet = self._doc.add_sheet(sheet if sheet else 'Sheet')
        self.__num_row = 0
        self.write_list(self.fieldnames)

    def write_row(self, **row) -> None:
        sheet_row = self.sheet.row(self.__num_row)
        for i, field in enumerate(self.fieldnames):
            sheet_row.write(i, row[field])
        self.__num_row += 1

    def close(self) -> None:
        self._doc.save(self.file_name)
