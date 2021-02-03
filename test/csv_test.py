import os
import unittest

from tqdm import tqdm

from filedatasource import CsvWriter, CsvReader, ExcelWriter, ExcelReader

DATA_FILE = 'data.csv'
COMPRESSED_FILE = 'data.csv.gz'
EXCEL_FILE = 'data.xlsx'


def write_registers(writer):
    writer.write_row(a=1, b=2, c=3)
    writer.write_row(a=2, b=4, c=7)
    writer.write_row(a=3, b=6, c=15)
    writer.write_dict({'a': 4, 'b': 8, 'c': 31})


class Employee(object):
    @property
    def full_name(self) -> str:
        return self.name + ' ' + self.surname

    @property
    def name(self) -> str:
        return self.__name

    @property
    def surname(self) -> str:
        return self.__surname

    def __init__(self, name: str, surname: str):
        self.__name = name
        self.__surname = surname


class MyTestCase(unittest.TestCase):
    def test_write_csv_dict(self):
        with CsvWriter(DATA_FILE, fieldnames=['a', 'b', 'c']) as writer:
            write_registers(writer)
        self.assertTrue(os.path.exists(DATA_FILE))
        with CsvReader(DATA_FILE) as reader:
            for obj in tqdm(reader):
                pass
        self.assertEqual(obj.b, '8')
        os.remove(DATA_FILE)

    def test_write_csv_obj(self):
        with CsvWriter(COMPRESSED_FILE, fieldnames=Employee) as writer:
            writer.write(Employee('John', 'Smith'))
            writer.write(Employee('Maria', 'Ortega'))
        with CsvReader(COMPRESSED_FILE) as reader:
            obj = next(reader)
            self.assertEqual(obj.name, 'John')
            self.assertEqual(obj.surname, 'Smith')
            obj = next(reader)
            self.assertEqual(obj.name, 'Maria')
            self.assertEqual(obj.surname, 'Ortega')
            with self.assertRaises(StopIteration):
                reader.read()
        os.remove(COMPRESSED_FILE)

    def test_write_excel(self):
        with ExcelWriter(EXCEL_FILE, fieldnames=['a', 'b', 'c']) as writer:
            write_registers(writer)
        self.assertTrue(os.path.exists(EXCEL_FILE))
        with ExcelReader(EXCEL_FILE) as reader:
            for obj in tqdm(reader):
                pass
        self.assertEqual(obj.b, 8)
        os.remove(EXCEL_FILE)

    def test_import(self):
        with CsvWriter(DATA_FILE, fieldnames=['a', 'b', 'c']) as writer:
            write_registers(writer)
        self.assertTrue(os.path.exists(DATA_FILE))
        with CsvReader(DATA_FILE) as reader:
            with ExcelWriter(EXCEL_FILE, fieldnames=reader.fieldnames) as writer:
                writer.import_reader(reader)
        self.assertTrue(os.path.exists(EXCEL_FILE))
        os.remove(DATA_FILE)
        os.remove(EXCEL_FILE)


if __name__ == '__main__':
    unittest.main()
