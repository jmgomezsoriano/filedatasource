from abc import ABC, ABCMeta, abstractmethod
from collections import namedtuple
from inspect import getmembers, isroutine
from typing import List, Union, TextIO, BinaryIO, Any, Dict, Sequence


class DataFile(ABC):
    """
    Abstract class for object that deals with Data files.
    """
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def fieldnames(self) -> List[str]:
        """
        :return: The sequence of field names to use as CSV head.
        """
        pass

    @property
    def file_name(self) -> str:
        """
        :return: The file name.
        """
        return self._fname

    def __init__(self, file_or_io: Union[str, TextIO, BinaryIO]):
        """
        Constructor.
        :param file_or_io: The file path to the Data file.
        """
        self._fname = file_or_io if isinstance(file_or_io, str) else None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    @abstractmethod
    def close(self) -> None:
        """

        :return:
        """
        pass

    @staticmethod
    def attributes2dict(obj: Union[object]) -> Dict[str, Any]:
        members = getmembers(obj, lambda member: not (isroutine(member)))
        return {att[0]: att[1] for att in members if not att[0].startswith('_')}

    @staticmethod
    def attributes2list(obj: Union[object]) -> List[str]:
        members = getmembers(obj, lambda member: not (isroutine(member)))
        return [att[0] for att in members if not att[0].startswith('_')]

    @staticmethod
    def dict2obj(d: dict) -> object:
        keys = [key.replace(' ', '_') for key in d.keys()]
        return namedtuple('Row', keys)(*d.values()) if d else None


class DataWriter(DataFile, ABC):
    __metaclass__ = ABCMeta

    def _parse_fieldnames(self, fieldnames: Union[List[str], object]) -> List[str]:
        if isinstance(fieldnames, List):
            return fieldnames
        if isinstance(fieldnames, object):
            return self.attributes2list(fieldnames)
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
        self.write_row(**self.attributes2dict(o))

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
        self.write_row(**{field: l[i] for i, field in enumerate(self.fieldnames)})

    def import_reader(self, reader: 'DataReader'):
        for obj in reader:
            self.write(obj)


class DataReader(DataFile, ABC):
    __metaclass__ = ABCMeta

    def __iter__(self):
        return self

    def __next__(self):
        return self.read()

    def read(self) -> object:
        """ Read a row of the CSV file.

        :return: An Python object with fields that represents the information of the file. The name of these fields
        correspond with the name of the CSV head fields.
        """
        return self.dict2obj(self.read_row())

    def read_objects(self) -> List[object]:
        objects = []
        obj = self.read()
        while obj:
            objects.append(obj)
            obj = self.read()

        return objects

    @abstractmethod
    def read_row(self) -> object:
        """ Read a row of the CSV file.

        :return: An Python object with fields that represents the information of the file. The name of these fields
        correspond with the name of the CSV head fields.
        """
        pass

    def read_rows(self) -> List[object]:
        return [row for row in next(self)]
