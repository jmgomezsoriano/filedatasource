import gzip
from abc import ABC, ABCMeta
from csv import DictWriter, DictReader
from enum import Enum
from inspect import getmembers, isroutine
from typing import Sequence, Union, TextIO, BinaryIO, List

from filedatasource.datafile import DataFile, DataReader


class Mode(Enum):
    APPEND = 'a'
    WRITE = 'w'


class Csv(DataFile, ABC):
    """
    Abstract class for object that deals with CSV files.
    """
    __metaclass__ = ABCMeta

    @property
    def encoding(self) -> str:
        return self.__encoding

    def __init__(self, file_or_io: [str, TextIO, BinaryIO], encoding: str = 'utf-8'):
        super().__init__(file_or_io)
        self.__encoding = encoding


class CsvWriter(Csv):
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

    def __init__(self, file_or_io: Union[str, TextIO, BinaryIO], fieldnames: List[str] =None,
                 mode: Mode = Mode.WRITE, encoding: str = 'utf-8'):
        """ Constructor of this CSV writer.

        :param file_or_io: The file path or an opened stream to use. If it is a file path and it ends in .gz, then
        a compressed file is created using gzip.
        :param fieldnames: The field names of this CSV.
        :param mode: The writing mode: Mode.APPEND or Mode.WRITE. By default Mode.WRITE.
        :param encoding: The encoding (it is only used if the parameter file_or_io is a file path).
        """
        super().__init__(file_or_io, encoding)
        self._fieldnames = fieldnames if fieldnames else []
        if isinstance(file_or_io, str):
            open_func = gzip.open if file_or_io.endswith('gz') else open
            self._file = open_func(file_or_io, f'{mode.value}t', encoding=self.encoding)

        self._writer = DictWriter(self._file, fieldnames=self.fieldnames)
        if mode == Mode.WRITE:
            self._writer.writeheader()

    def write_row(self, **row) -> None:
        """ Write a row.

        :param row: The dictionary or parameters to write.
        """
        self._writer.writerow(row)

    def write(self, o: object) -> None:
        """ Write a row.

        :param o: An object with public attributes or properties.
        """
        members = getmembers(o, lambda member: not (isroutine(member)))
        attributes = {att[1]: att[1] for att in members if not att[0].startswith('_')}
        self._writer.writerow(**attributes)

    def write_rows(self, rows: Sequence[dict]) -> None:
        """
        Write a sequence of rows.

        :param rows: The sequence of rows to write.
        """
        for row in rows:
            self._writer.writerow(row)

    def write_objects(self, objects: Sequence[object]) -> None:
        """
        Write a sequence of objects.

        :param objects: The sequence of objects to write with public attributes or properties.
        """
        for o in objects:
            self.write(o)


class CsvReader(Csv, DataReader):
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
        super(CsvReader, self).__init__(file_or_io, encoding)
        if isinstance(file_or_io, str):
            self._file = self.__open_file(file_or_io)
        else:
            self._file = file_or_io
        self._reader = DictReader(self._file)

    def __open_file(self, fname: str):
        open_func = gzip.open if fname.endswith('.gz') else open
        return open_func(fname, 'rt', encoding=self.encoding)

    def read_row(self) -> object:
        """ Read a row of the CSV file.

        :return: An Python object with fields that represents the information of the file. The name of these fields
        correspond with the name of the CSV head fields.
        """
        return next(self._reader)
