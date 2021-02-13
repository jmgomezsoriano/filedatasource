# File data-source
Convert several file data sources (like typical CSV or Excel) to Python objects or dictionaries in an easy way.

## Install

```shell script
pip install filedatasource
```
If you want to read an Excel file in xlsx format, you need to install the openpyxl module:

```shell script
pip install openpyxl
```
If you want to create an Excel file in xlsx format, you need to install the xlsxwriter module:

```shell script
pip install xlsxwriter
```

If you want to read an Excel file in old xls format, you need to install the __xlrd__ module:

```shell script
pip install xlrd
```

And, if you want to write into an old xls format, you need to install the __xlwt__ module:

```shell script
pip install xlwt
```

## How to use
File data-source is a Python module that allows to extract the data form typical CSV or Excel files with the
following format:

```text
field_1,field_2,field_3,...
cell_1_1,cell_1_2,cell_1_3,...
cell_2_1,cell_2_2,cell_3_3,...
...
```

That means, the first line for the column names, and the rest of rows are the value of that columns. 
For example, if we have this **data.csv** file:

```text
name,surname,address
Jhon,Smith,Oxford street
Maria,Ortega,George Washington street 
```

**Note**: This module does not work with different CSV formats. If you need to parse more complex files, you need to use
Panda or native modules as openpyxl or xlsxwriter. This module is thought for parsing or generating typical data sources
based on files in data scientists processes.

##  How to read

The simplest code will be:

```python
from filedatasource import CsvReader

with CsvReader('data.csv') as reader:
    for person in reader:
        print(person.name, person.surname, person.address)
```

If the file name ends with .gz then, CsvReader() will decompress during the reading. 
By default, ExcelReader or CsvReader obtain objects with the fieldnames as attributes. 
If the field name has a character that is not valid as Python identifier, it will be replaced by _. 
If the field name starts with a number, then the character 'n' is added at the beginning. 
For example, if you have the following data file in CSV:

```text
1d,D&D,Figures
20,Main dice all
...
```

The identifier for the object attributes will be __n1d__, __D_D__ and __Figure__, respectively.

**Important note**: All the data extracted with CsvReader will be of type str.

If you want to get list of values or list of dictionaries instead an object, you can change the parameter __mode__:

```python
from filedatasource import CsvReader, ReadMode

# To get list of values
with CsvReader('data.csv', mode=ReadMode.LIST) as reader:
    for person in reader:
        print(person[0], person[1], person[2])

# To get list of dictionaries
with CsvReader('data.csv', mode=ReadMode.DICT) as reader:
    for person in reader:
        print(person['name'], person['surname'], person['fullname'])
```

Moreover, it could read xls and xlsx files using the class ExcelReader.
To read the **data.xlsx** file with the following content is very similar:

|name |surname|address                 |
|-----|-------|------------------------|
|Jhon |Smith  |Oxford street           |
|Maria|Ortega |George Washington street|

The simplest code will be:

```python
from filedatasource import ExcelReader

with ExcelReader('data.xslx') as reader:
    for person in reader:
        print(person.name, person.surname, person.address)
```

If the file name ends with **.xls** instead of **.xlsx**, this class will read it correctly too.

Regardless of using CsvReader or ExcelReader, you can use the **tqdm()** method to measure the time that
you process will take:

```python
from filedatasource import ExcelReader, CsvReader
from tqdm import tqdm

with ExcelReader('data.xslx') as reader:
    for person in tqdm(reader, desc='Reading the Excel file'):
        print(person.name, person.surname, person.address)

with CsvReader('data.xslx') as reader:
    for person in tqdm(reader, desc='Reading the CSV file'):
        print(person.name, person.surname, person.address)
```

However, the CsvReader needs, previously, to pre-read the entire file to calculate the number of rows, and it might take
a bit longer. This problem does not occur with the Excel file because it is fully loaded into memory.

## How to write a data file

With file data-source is very easy to write, both, a CSV file (compressed or not) and a Excel file (xls or xlsx).
Only you need to use CsvWriter or ExcelWriter writing the rows by parameters, with a list of values or 
with a dictionary. For example:

```python
from filedatasource import CsvWriter

# Writing a row by means of parameters, a list of values or a dictionary.
with CsvWriter('data.csv.gz', fieldnames=['a', 'b', 'c']) as writer:
    writer.write_row(a=1, b=2, c=3)
    writer.write([2, 4, 7])
    writer.write({'a': 4, 'b': 8, 'c': 31})
```

If the file name ends with .gz, it will be compressed automatically. Moreover, you can store an object like this:

```python
from filedatasource import CsvWriter

class Example(object):
    def __init__(self, a: int, b: int, c: int):
        self.a = a
        self.b = b
        self.c = c

# Writing with Python objects
with CsvWriter('data.csv.gz', fieldnames=['a', 'b', 'c']) as writer:
    writer.write(Example(1, 2, 3))
    writer.write(Example(4, 5, 6))
```

If you in your object class defines properties, you can use it directly as fieldnames. For example:

```python
from filedatasource import CsvWriter

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

# Writing an object and defining the fieldnames automatically from the object property
with CsvWriter('data.csv', fieldnames=Employee) as writer:
    writer.write(Employee('John', 'Smith'))
    writer.write(Employee('Maria', 'Ortega'))
```

By default, using CsvWriter class, if the file 'data.csv' exists, it will be removed.
In order to avoid it and add the rows at the end of the file, you can use the __mode__ parameter like this:

```python
from filedatasource import CsvWriter, Mode

# Creating a CsvWriter in APPEND mode
with CsvWriter('data.csv', mode=Mode.APPEND) as writer:
    writer.write_dicts([
        {'a': 10, 'b': 11, 'c': 12},
        {'a': 13, 'b': 14, 'c': 15}
    ])
```

The __mode__ parameter can only be used in CSV files and not in Excel files.

## Working with Excel sheets

__ExcelReader__ only works with one Excel sheet at a time. You can select the sheet to read using the parameter 
__sheet__ both using the sheet name or the sheet number (starting by 0). For eample:

```python
from filedatasource import ExcelReader

# Reading the first sheet of the file 'Example.xls'
with ExcelReader('Example.xls', sheet=0) as reader:
    for row in reader:
        print(row)
# Reading the second sheet of the file 'Example.xls'
with ExcelReader('Example.xls', sheet=1) as reader:
    for row in reader:
        print(row)
# Reading the sheet named 'Clients' of the file 'Example.xls'
with ExcelReader('Example.xls', sheet='Clients') as reader:
    for row in reader:
        print(row)
# Reading the sheet named 'Suppliers' of the file 'Example.xls'
with ExcelReader('Example.xls', sheet='Suppliers') as reader:
    for row in reader:
        print(row)
```

## Reading and writing whole files

With __file datasource__ you can read or write a whole data file in two lines using __DataWriter.write_lists()__,
__DataWriter.write_dicts()__, and __DataWriter.write_objects()__ for writing list of lists, dictionaries and object,
respectively; and __DataReader.read_lists()__, __DataReader.read_rows()__, and __DataReader.read_objects()__ for 
getting a list of lists, dictionaries or objects with the all the file data.

For example, writing several rows:

```python
from filedatasource import CsvWriter

with CsvWriter('data.xlsx', fieldnames=['a', 'b', 'c']) as writer:
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
```
All these methods also work with ExcelWriter. However, it could be written only with one line:

```python
from filedatasource import list2csv, dict2csv, objects2csv
from filedatasource import list2excel, dict2excel, objects2excel

data_list = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
data_dict = [
    {'a': 10, 'b': 11, 'c': 12},
    {'a': 13, 'b': 14, 'c': 15}
]
data_objects = [
    Example(16, 17, 18),
    Example(19, 20, 21),
    Example(22, 23, 24)
]

# Write a list of lists into a CSV file
list2csv('data.csv', data_list, fieldnames=['a', 'b', 'c'])
# Write a list of dicts into a CSV file
dict2csv('data.csv', data_dict, fieldnames=['a', 'b', 'c'])
# Write a list of objects into a CSV file
objects2csv('data.csv', data_objects, fieldnames=['a', 'b', 'c'])
# Write a list of lists into a Excel file
list2excel('data.xlsx', data_list, fieldnames=['a', 'b', 'c'])
# Write a list of dicts into a Excel file
dict2excel('data.xlsx', data_dict, fieldnames=['a', 'b', 'c'])
# Write a list of objects into a Excel file
objects2excel('data.xlsx', data_objects, fieldnames=['a', 'b', 'c'])
```

For reading a whole file, you only need to write the following sentences:

```python
from filedatasource import CsvReader, ExcelReader

# Read a whole compressed CSV file and get a list of lists
with CsvReader('data.csv.gz') as reader:
    lists = reader.read_lists()
fieldnames = reader.fieldnames  # This line is only necessary if you want to get the fieldnames for read_lists()
print(fieldnames[0], lists[0][0])
    
# Read a whole CSV file and obtain a list of dictionaries, with the fieldnames as key and the data the values.
with CsvReader('data.csv') as reader:
    dicts = reader.read_rows()
print(lists[0]['name'])

# Read a whole Excel file and obtain a list of objects, with the fieldnames as object attributes
with ExcelReader('data.xlsx') as reader:
    objs = reader.read_objects()
print(lists[0].name)
```

And, you can also use the equivalent functions **list2csv()**, **dict2csv()**, **objects2csv()**,
**list2excel()**, **dict2excel()**, and **objects2excel()**. For example:

```python
from filedatasource import csv2list, csv2dict, excel2objects

# Read a whole compressed CSV file and get a list of lists
lists = csv2list('data.csv.gz')
print(lists[0][0])

# Read a whole CSV file and obtain a list of dictionaries, with the fieldnames as key and the data the values.
dicts = csv2dict('data.csv')
print(lists[0]['name'])

# Read a whole Excel file and obtain a list of objects, with the fieldnames as object attributes
objs = excel2objects('data.xlsx')
print(lists[0].name)
```

## Convert from CSV to Excel and viceversa

With these tools, it is very simply to convert from a Csv to an Excel file and viceversa:

```python
from filedatasource import ExcelWriter, CsvReader

with CsvReader('data.csv') as reader:
    with ExcelWriter('data.xlsx', fieldnames=reader.fieldnames) as writer:
        for obj in reader:
            writer.write(obj)
```

However, it can be made easier: 

```python
from filedatasource import ExcelWriter, CsvReader

with CsvReader('data.csv') as reader:
    with ExcelWriter('data.xlsx', fieldnames=reader.fieldnames) as writer:
        writer.import_reader(reader)
```

If you are using the same Writer several times, you can use a subclass in order to avoid define the fieldnames several
times overwritting the fieldnames property. For example:

```python
from filedatasource import CsvWriter, Mode
from typing import List

class TestWriter(CsvWriter):
    @property
    def fieldnames(self) -> List[str]:
        return ['a', 'b', 'c']

with TestWriter('data.csv') as writer:
    writer.write_lists([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])
with TestWriter(('data.csv', mode=Mode.APPEND) as writer:
    writer.write_dicts([
        {'a': 10, 'b': 11, 'c': 12},
        {'a': 13, 'b': 14, 'c': 15}
    ])
```

## Builders

You have two builders to create readers or writers based on the file extension with default arguments.

```python
from filedatasource import open_reader, open_writer

# Read a CSV
with open_reader('data.csv') as reader:
    ...

# Read a compressed CSV
with open_reader('data.csv.gz') as reader:
    ...

# Read the first sheet from a Excel
with open_reader('data.xlsx') as reader:
   ...

# Write a CSV
with open_writer('data.csv', fieldnames=[...]) as writer:
    ...

# Write a compressed CSV1
with open_writer('data.csv.gz', fieldnames=[...]) as writer:
    ...

# Write a Excel file creating a default sheet
with open_writer('data.xlsx', fieldnames=[...]) as writer:
   ...
```