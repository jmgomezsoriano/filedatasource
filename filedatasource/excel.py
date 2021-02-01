from typing import Union, List

from filedatasource.datafile import DataReader


class ExcelReader(DataReader):
    @property
    def fieldnames(self) -> List[str]:
        return self.__fieldnames

    @property
    def sheet(self) -> str:
        return self.__sheet

    def __init__(self, fname: str, sheet: Union[str, int] = None):
        super().__init__(fname)
        self.__fieldnames = []
        self.__sheet_name = sheet
        try:
            xlrd = __import__('xlrd')
        except ImportError:
            raise ModuleNotFoundError('xlrd is required. Please, install it with:\n\npip install xlrd')
        self.__doc = xlrd.open_workbook(fname)
        sheet = sheet if sheet else 0
        self.__sheet = self.__doc.sheet_by_name(sheet) if isinstance(sheet, str) else self.__doc.sheet_by_index(sheet)
        self.__row = 0
        self.__fieldnames = [cell.value for cell in self.__sheet.row(self.__row)]

    def read_row(self) -> object:
        if self.__row < self.__sheet.nrows - 1:
            self.__row += 1
            row = self.__sheet.row(self.__row)
            return {self.fieldnames[i]: cell.value for i, cell in enumerate(row)}
        raise StopIteration()

    def __len__(self) -> int:
        return self.__sheet.nrows
