import gzip
from abc import ABC, ABCMeta
from csv import DictWriter, DictReader
from enum import Enum
from typing import Union, TextIO, BinaryIO, List

from filedatasource.datafile import DataFile, DataReader, DataWriter


class Mode(Enum):
    APPEND = 'a'
    WRITE = 'w'
    READ = 'r'


def open_file(fname: str, mode: Mode, encoding: str):
    open_func = gzip.open if fname.endswith('.gz') else open
    return open_func(fname, f'{mode.value}t', encoding=encoding, newline='')


class CsvData(DataFile, ABC):
    """
    Abstract class for object that deals with CSV files.
    """
    __metaclass__ = ABCMeta

    @property
    def encoding(self) -> str:
        """
        :return: The file encoding.
        """
        return self.__encoding

    def __init__(self, file_or_io: [str, TextIO, BinaryIO], mode: Mode, encoding: str = 'utf-8'):
        super().__init__(file_or_io)
        self.__encoding = encoding
        self._file = open_file(file_or_io, mode, self.encoding) if isinstance(file_or_io, str) else file_or_io

    def close(self) -> None:
        self._file.close()


class CsvWriter(CsvData, DataWriter):
    """
    A CSV writer to create a typical CSV file with head. It is very easy to use, only need to

    .. code-block:: python

        fieldnames = ['id', 'name', 'surname', 'address']
        with ConflictsWriter('data.csv', fieldnames) as writer:
            writer.write_row(id=1, name='John', surname='Smith', address='Oxford street')

    Also, if the file ends with .gz, the file will be compressed with gzip automatically.
    """
    @property
    def fieldnames(self) -> List[str]:
        """
        :return: The sequence of field names to use as CSV head.
        """
        return self._fieldnames

    def __init__(self, file_or_io: Union[str, TextIO, BinaryIO], fieldnames: Union[List[str], type, object] = None,
                 mode: Mode = Mode.WRITE, encoding: str = 'utf-8'):
        """ Constructor of this CSV writer.

        :param file_or_io: The file path or an opened stream to use. If it is a file path and it ends in .gz, then
        a compressed file is created using gzip.
        :param fieldnames: The field names of this CSV.
        :param mode: The writing mode: Mode.APPEND or Mode.WRITE. By default Mode.WRITE.
        :param encoding: The encoding (it is only used if the parameter file_or_io is a file path).
        """
        if mode not in [Mode.WRITE, Mode.APPEND]:
            raise ValueError(f'The {type(self).__name__} only allows modes {Mode.WRITE} or {Mode.APPEND}, not {mode}')
        super().__init__(file_or_io, mode, encoding)
        # CsvData.__init__(file_or_io, mode,  mode, encoding)
        # super().__init__(file_or_io, mode,  mode, encoding)
        self._fieldnames = self._parse_fieldnames(fieldnames)

        self._writer = DictWriter(self._file, fieldnames=self.fieldnames)
        if mode == Mode.WRITE:
            self._writer.writeheader()

    def write_row(self, **row) -> None:
        """ Write a row.

        :param row: The dictionary or parameters to write.
        """
        self._writer.writerow(row)


class CsvReader(CsvData, DataReader):
    """
    A CSV reader to read a typical CSV file with head. It is very easy to use. For example, if the file 'data.csv'
    contains:

    .. code-block:
        id,name,surname,address
        1,John,Smith,Oxford street
        ---

    It is only necessary to write:

    .. code-block:: python

        with ConflictsWriter('data.csv') as reader:
            for row in reader:
                print(row.id, row.name, row.surname, row.address)

    Also, if the file ends with .gz, the file will be read from a compressed file with gzip automatically.
    """
    @property
    def fieldnames(self) -> List[str]:
        """
        :return: The sequence of field names to use as CSV head.
        """
        return self._reader.fieldnames

    def __init__(self, file_or_io: Union[str, TextIO, BinaryIO], encoding: str = 'utf-8'):
        """ Constructor of this CSV reader.

        :param file_or_io: The file path or an opened stream to use. If it is a file path and it ends in .gz, then
        the compressed file is read using gzip.
        :param encoding: The encoding (it is only used if the parameter file_or_stram is a file path).
        """
        super(CsvReader, self).__init__(file_or_io, Mode.READ, encoding)
        self._reader = DictReader(self._file)

    def read_row(self) -> dict:
        """ Read a row of the CSV file.

        :return: An Python object with fields that represents the information of the file. The name of these fields
        correspond with the name of the CSV head fields.
        """
        return next(self._reader)

    def __len__(self) -> int:
        if self.file_name:
            with CsvReader(self.file_name, self.encoding) as reader:
                return sum(1 for _ in reader)
        return 0
