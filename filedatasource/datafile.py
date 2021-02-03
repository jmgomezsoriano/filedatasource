from abc import ABC, ABCMeta, abstractmethod
from enum import Enum, unique, auto
from typing import List, Union, TextIO, BinaryIO, Any, Dict, Sequence, Iterable

from filedatasource.utils import dict2obj, attributes2list, attributes2dict, dict2list, dict_keys2list, to_identifier


@unique
class ReadMode(Enum):
    OBJECT = auto()
    DICT = auto()
    LIST = auto()


class DataFile(ABC):
    """
    Abstract class for object that deals with data files.
    """
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def fieldnames(self) -> List[str]:
        """ :return: The sequence of field names to use as CSV head. """
        pass

    @property
    def file_name(self) -> str:
        """ :return: The file name. """
        return self._fname

    def __init__(self, file_or_io: Union[str, TextIO, BinaryIO]):
        """ Constructor.
        :param file_or_io: The file path to the Data file.
        """
        self._fname = file_or_io if isinstance(file_or_io, str) else None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    @abstractmethod
    def close(self) -> None:
        """ This method is called when finishes with this object. """
        pass


class DataWriter(DataFile, ABC):
    __metaclass__ = ABCMeta

    def _parse_fieldnames(self, fieldnames: Union[List[str], object]) -> List[str]:
        if isinstance(fieldnames, List):
            return fieldnames
        if isinstance(fieldnames, dict):
            return dict_keys2list(fieldnames)
        if isinstance(fieldnames, object):
            return attributes2list(fieldnames)
        return []

    @abstractmethod
    def write_row(self, **row) -> None:
        """ Write a row.

        :param row: The dictionary or parameters to write.
        """
        pass

    def write_dict(self, row) -> None:
        self.write_row(**row)

    def write(self, o: object) -> None:
        """ Write a row.

        :param o: An object with public attributes or properties.
        """
        self.write_row(**attributes2dict(o))

    def write_rows(self, rows: Sequence[dict]) -> None:
        """
        Write a sequence of rows.

        :param rows: The sequence of rows to write.
        """
        for row in rows:
            self.write_row(**row)

    def write_objects(self, objects: Sequence[object]) -> None:
        """
        Write a sequence of objects.

        :param objects: The sequence of objects to write with public attributes or properties.
        """
        for o in objects:
            self.write(o)

    def write_list(self, l: list) -> None:
        self.write_dict({field: l[i] for i, field in enumerate(self.fieldnames)})

    def import_reader(self, reader: 'DataReader'):
        for obj in reader:
            self.write(obj)


class DataReader(DataFile, ABC):
    __metaclass__ = ABCMeta

    def __init__(self, file_or_io: Union[str, TextIO, BinaryIO], mode: ReadMode = ReadMode.OBJECT):
        super().__init__(file_or_io)
        self.__mode = mode

    def __iter__(self):
        return self

    def __next__(self):
        return self.read()

    def read(self) -> object:
        """ Read a row of the CSV file.

        :return: An Python object with fields that represents the information of the file. The name of these fields
        correspond with the name of the CSV head fields.
        """
        if self.__mode == ReadMode.DICT:
            return dict2obj(self.read_row())
        elif self.__mode == ReadMode.OBJECT:
            return dict2obj(self.read_row())
        return dict2list(self.read_row())

    def read_objects(self) -> List[object]:
        objects = []
        obj = self.read()
        while obj:
            objects.append(obj)
            obj = self.read()

        return objects

    @abstractmethod
    def read_row(self) -> dict:
        """ Read a row of the CSV file.

        :return: An Python object with fields that represents the information of the file. The name of these fields
        correspond with the name of the CSV head fields.
        """
        pass

    def read_rows(self) -> List[object]:
        return [row for row in next(self)]
