import os
import unittest
from typing import List

from tqdm import tqdm

from filedatasource import CsvWriter, CsvReader, ExcelWriter, ExcelReader, Mode, ReadMode, DataWriter, DataReader

DATA_FILE = 'data.csv'
COMPRESSED_FILE = 'data.csv.gz'
EXCEL_FILE = 'data.xlsx'
XLS_FILE = 'data.xls'


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


class Example(object):
    def __init__(self, a: int, b: int, c: int):
        self.a, self.b, self.c = a, b, c


class TestWriter(CsvWriter):
    @property
    def fieldnames(self) -> List[str]:
        return ['a', 'b', 'c']


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
        with ExcelWriter(EXCEL_FILE, fieldnames=['a', 'b', 'c']) as writer:
            write_registers(writer)
        self.assertTrue(os.path.exists(EXCEL_FILE))
        with ExcelReader(EXCEL_FILE) as reader:
            with CsvWriter(DATA_FILE, fieldnames=reader.fieldnames) as writer:
                writer.import_reader(reader)
        self.assertTrue(os.path.exists(DATA_FILE))
        os.remove(DATA_FILE)
        os.remove(EXCEL_FILE)

    def test_dict_2_object(self):
        d = {'1': 1, 'G&S': 2}
        with CsvWriter(DATA_FILE, fieldnames=d) as writer:
            writer.write_dict(d)
            writer.write_list(list(d.values()))
        with CsvReader(DATA_FILE) as reader:
            for obj in reader:
                pass
        self.assertEqual(obj.n1, '1')
        self.assertEqual(obj.G_S, '2')
        os.remove(DATA_FILE)

    def test_lists(self):
        with CsvWriter(DATA_FILE, fieldnames=['a', 'b', 'c']) as writer:
            self.__write_lists(writer)
        with CsvReader(DATA_FILE) as reader:
            self.check_lists_csv(reader)
        with CsvReader(DATA_FILE) as reader:
            self.check_dicts(reader)
        with CsvReader(DATA_FILE) as reader:
            self.check_objects(reader)
        os.remove(DATA_FILE)

    def check_lists_csv(self, reader: DataReader):
        lists = reader.read_lists()
        self.assertEqual(len(lists), 8)
        self.assertListEqual(lists[0], ['1', '2', '3'])
        self.assertListEqual(lists[7], ['22', '23', '24'])

    def check_lists_excel(self, reader: DataReader):
        lists = reader.read_lists()
        self.assertEqual(len(lists), 8)
        self.assertListEqual(lists[0], [1, 2, 3])
        self.assertListEqual(lists[7], [22, 23, 24])

    def check_dicts(self, reader: DataReader):
        dicts = reader.read_rows()
        self.assertEqual(len(dicts), 8)
        self.assertDictEqual(dicts[0], {'a': '1', 'b': '2', 'c': '3'})
        self.assertDictEqual(dicts[7], {'a': '22', 'b': '23', 'c': '24'})

    def check_objects(self, reader: DataReader):
        objs = reader.read_objects()
        self.assertEqual(len(objs), 8)
        self.assertEqual(objs[0].a, '1')
        self.assertEqual(objs[0].b, '2')
        self.assertEqual(objs[0].c, '3')
        self.assertEqual(objs[7].b, '23')
        self.assertEqual(objs[7].c, '24')

    def __write_lists(self, writer: DataWriter):
        writer.write_lists([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])
        writer.write_dicts([
            {'a': 10, 'b': 11, 'c': 12},
            {'a': 13, 'b': 14, 'c': 15}
        ])
        writer.write_objects([
            Example(16, 17, 18),
            Example(19, 20, 21),
            Example(22, 23, 24)
        ])

    def test_read_modes(self):
        with CsvWriter(DATA_FILE, fieldnames=['a', 'b', 'c']) as writer:
            self.__write_lists(writer)
        with CsvReader(DATA_FILE, mode=ReadMode.DICT) as reader:
            for obj in reader:
                pass
        self.assertDictEqual(obj, {'a': '22', 'b': '23', 'c': '24'})
        with CsvReader(DATA_FILE, mode=ReadMode.LIST) as reader:
            for obj in reader:
                pass
        self.assertListEqual(obj, ['22', '23', '24'])
        with CsvReader(DATA_FILE, mode=ReadMode.OBJECT) as reader:
            for obj in reader:
                pass
        self.assertEqual(obj.b, '23')
        self.assertEqual(obj.c, '24')
        os.remove(DATA_FILE)

    def test_append(self):
        with TestWriter(COMPRESSED_FILE) as writer:
            writer.write_lists([
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]
            ])
        with TestWriter(COMPRESSED_FILE, mode=Mode.APPEND) as writer:
            writer.write_dicts([
                {'a': 10, 'b': 11, 'c': 12},
                {'a': 13, 'b': 14, 'c': 15}
            ])
        with CsvReader(COMPRESSED_FILE, mode=ReadMode.OBJECT) as reader:
            self.assertListEqual(reader.read_list(), ['1', '2', '3'])
            for obj in reader:
                pass
        self.assertEqual(obj.b, '14')
        self.assertEqual(obj.c, '15')

    def test_xls_xlsx(self):
        with ExcelWriter(EXCEL_FILE, fieldnames=['a', 'b', 'c']) as writer:
            self.__write_lists(writer)
        with ExcelReader(EXCEL_FILE) as reader:
            self.check_lists_excel(reader)
        with ExcelWriter(XLS_FILE, fieldnames=['a', 'b', 'c']) as writer:
            self.__write_lists(writer)
        with ExcelReader(XLS_FILE) as reader:
            self.check_lists_excel(reader)


if __name__ == '__main__':
    unittest.main()
