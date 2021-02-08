import os
import unittest
from typing import List

from tqdm import tqdm

from filedatasource import CsvWriter, CsvReader, ExcelWriter, ExcelReader, Mode, ReadMode, DataWriter, DataReader, \
    open_reader, open_writer, excel2list, excel2dict, csv2dict, csv2objects, objects2csv, dict2csv, list2csv, csv2list

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


lists = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
dicts = [
    {'a': 10, 'b': 11, 'c': 12},
    {'a': 13, 'b': 14, 'c': 15}
]
objects = [
    Example(16, 17, 18),
    Example(19, 20, 21),
    Example(22, 23, 24)
]


class TestWriter(CsvWriter):
    @property
    def fieldnames(self) -> List[str]:
        return ['a', 'b', 'c']


def list_to_int(lists: List[List[str]]) -> List[List[int]]:
    r = []
    for lst in lists:
        r.append([int(x) for x in lst])
    return r


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
            self.__write_lists_writer(writer)
        with CsvReader(DATA_FILE) as reader:
            self.check_lists_reader(reader)
        with CsvReader(DATA_FILE) as reader:
            self.check_dicts_reader(reader)
        with CsvReader(DATA_FILE) as reader:
            self.check_objects_reader(reader)
        os.remove(DATA_FILE)

    def check_lists_csv(self, lists):
        self.assertEqual(len(lists), 8)
        self.assertListEqual(lists[0], ['1', '2', '3'])
        self.assertListEqual(lists[7], ['22', '23', '24'])

    def check_lists_reader(self, reader: DataReader):
        lists = reader.read_lists()
        if isinstance(reader, CsvReader):
            self.check_lists_csv(lists)
        else:
            self.check_lists_excel(lists)

    def check_lists_excel(self, lists):
        self.assertEqual(len(lists), 8)
        self.assertListEqual(lists[0], [1, 2, 3])
        self.assertListEqual(lists[7], [22, 23, 24])

    def check_dicts_reader(self, reader: DataReader):
        dicts = reader.read_rows()
        if isinstance(reader, CsvReader):
            self.check_dicts_csv(dicts)
        else:
            self.check_dicts_excel(dicts)

    def check_dicts_csv(self, dicts):
        self.assertEqual(len(dicts), 8)
        self.assertDictEqual(dicts[0], {'a': '1', 'b': '2', 'c': '3'})
        self.assertDictEqual(dicts[7], {'a': '22', 'b': '23', 'c': '24'})

    def check_dicts_excel(self, dicts):
        self.assertEqual(len(dicts), 8)
        self.assertDictEqual(dicts[0], {'a': 1, 'b': 2, 'c': 3})
        self.assertDictEqual(dicts[7], {'a': 22, 'b': 23, 'c': 24})

    def check_objects_reader(self, reader: DataReader):
        objs = reader.read_objects()
        if isinstance(reader, CsvReader):
            self.check_objects_csv(objs)
        else:
            self.check_objects_excel(objs)

    def check_objects_csv(self, objs):
        self.assertEqual(len(objs), 8)
        self.assertEqual(objs[0].a, '1')
        self.assertEqual(objs[0].b, '2')
        self.assertEqual(objs[0].c, '3')
        self.assertEqual(objs[7].b, '23')
        self.assertEqual(objs[7].c, '24')

    def check_objects_excel(self, objs):
        self.assertEqual(len(objs), 8)
        self.assertEqual(objs[0].a, 1)
        self.assertEqual(objs[0].b, 2)
        self.assertEqual(objs[0].c, 3)
        self.assertEqual(objs[7].b, 23)
        self.assertEqual(objs[7].c, 24)

    def __write_lists_writer(self, writer: DataWriter):
        writer.write_lists(lists)
        writer.write_dicts(dicts)
        writer.write_objects(objects)

    def test_read_modes(self):
        with CsvWriter(DATA_FILE, fieldnames=['a', 'b', 'c']) as writer:
            self.__write_lists_writer(writer)
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
            writer.write_lists(lists)
        with TestWriter(COMPRESSED_FILE, mode=Mode.APPEND) as writer:
            writer.write_dicts(dicts)
        with CsvReader(COMPRESSED_FILE, mode=ReadMode.OBJECT) as reader:
            self.assertListEqual(reader.read_list(), ['1', '2', '3'])
            for obj in reader:
                pass
        self.assertEqual(obj.b, '14')
        self.assertEqual(obj.c, '15')

    def test_xls_xlsx(self):
        with ExcelWriter(EXCEL_FILE, fieldnames=['a', 'b', 'c']) as writer:
            self.__write_lists_writer(writer)
        with ExcelReader(EXCEL_FILE) as reader:
            self.check_lists_reader(reader)
        with ExcelWriter(XLS_FILE, fieldnames=['a', 'b', 'c']) as writer:
            self.__write_lists_writer(writer)
        with ExcelReader(XLS_FILE) as reader:
            self.check_lists_reader(reader)
        os.remove(EXCEL_FILE)
        os.remove(XLS_FILE)

    def test_builders(self):
        with open_writer(EXCEL_FILE, fieldnames=['a', 'b', 'c']) as writer:
            self.__write_lists_writer(writer)
        with ExcelReader(EXCEL_FILE) as reader:
            self.check_lists_reader(reader)
        self.check_lists_excel(excel2list(EXCEL_FILE))
        os.remove(EXCEL_FILE)
        with open_writer(XLS_FILE, fieldnames=['a', 'b', 'c']) as writer:
            self.__write_lists_writer(writer)
        with ExcelReader(XLS_FILE) as reader:
            self.check_dicts_reader(reader)
        self.check_dicts_excel(excel2dict(XLS_FILE))
        os.remove(XLS_FILE)
        with open_writer(DATA_FILE, fieldnames=['a', 'b', 'c']) as writer:
            self.__write_lists_writer(writer)
        with CsvReader(DATA_FILE) as reader:
            self.check_objects_reader(reader)
        self.check_objects_csv(csv2objects(DATA_FILE))
        os.remove(DATA_FILE)
        list2csv(COMPRESSED_FILE, lists, ['a', 'b', 'c'])
        self.assertListEqual(lists, list_to_int(csv2list(COMPRESSED_FILE)))
        dict2csv(COMPRESSED_FILE, dicts, ['a', 'b', 'c'])
        r = csv2dict(COMPRESSED_FILE)
        self.assertEqual(len(r), 2)
        self.assertDictEqual(r[0], {'a': '10', 'b': '11', 'c': '12'})
        self.assertDictEqual(r[1], {'a': '13', 'b': '14', 'c': '15'})
        objects2csv(COMPRESSED_FILE, objects, ['a', 'b', 'c'])
        with open_reader(COMPRESSED_FILE) as reader:
            obj = next(reader)
            self.assertEqual(obj.c, '18')
            obj = next(reader)
            self.assertEqual(obj.b, '20')
            obj = next(reader)
            self.assertEqual(obj.a, '22')
        os.remove(COMPRESSED_FILE)



if __name__ == '__main__':
    unittest.main()
