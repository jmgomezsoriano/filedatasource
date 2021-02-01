from abc import ABC, ABCMeta, abstractmethod
from collections import namedtuple
from typing import List, Union, TextIO, BinaryIO


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

    def __init__(self, file_or_io: Union[str, TextIO, BinaryIO]):
        """
        Constructor.
        :param file_or_io: The file path to the Data file.
        """
        self._fname = file_or_io if isinstance(file_or_io, str) else None
        self._file = None if isinstance(file_or_io, str) else file_or_io

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        """

        :return:
        """
        if self._file:
            self._file.close()


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
        d = self.read_row()
        return namedtuple('Row', d.keys())(*d.values()) if d else None

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
