# File data-source
The easiest way to parse CSV and Excel files, even compressed CSV files.

For example, with 2 or 1 line you can read a Excel or CSV file, even if it is a compressed CSV file:

```python
from filedatasource import open_reader, excel2objects
# Read a whole Excel file and obtain a list of objects,
# with the fieldnames as object attributes
with open_reader('data.csv.gz') as reader:
    objs = reader.read_objects()
print(objs[0].name)

# Or, even, easier:
objs = excel2objects('data.xlsx')
print(objs[0].name)

# If you do not want to load all the file to memory, you can do
with open_reader('data.csv.gz') as reader:
    for obj in reader:
       print(obj.name)
```


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

Finally, if you want to write into an old xls format, you need to install the __xlwt__ module:

```shell script
pip install xlwt
```

## For what kind of file formats it is used
**filedatasource** is a Python module that allows to extract the data form typical CSV or Excel files with the
following format:

```text
field_1,field_2,field_3,...
cell_1_1,cell_1_2,cell_1_3,...
cell_2_1,cell_2_2,cell_3_3,...
...
```

That means, the first row is used for the column names, and the rest of rows are the value of those columns. 
For example, with this **data.csv** file:

```text
name,surname,address
Jhon,Smith,Oxford street
Maria,Ortega,George Washington street 
```

Or an Excel file with the following content:

|name |surname|address                 |
|-----|-------|------------------------|
|Jhon |Smith  |Oxford street           |
|Maria|Ortega |George Washington street|

**Note**: This module does not work with other formats. If you need to parse more complex files, you need to use
Panda or native modules as openpyxl or xlsxwriter. This module is thought for parsing or generating typical data sources
based on files in data scientists processes.

##  How to read

The standard way to read a CSV is:

```python
from filedatasource import CsvReader

with CsvReader('data.csv') as reader:
    for person in reader:
        print(person.name, person.surname, person.address)
```

If the file name ends with .gz then, __CsvReader()__ will decompress the file during the reading. 
By default, __ExcelReader__ or __CsvReader__ obtain objects with the fieldnames as attributes. 

**Note**: All the data extracted with CsvReader will be of type str.

### Important note
This method is not recommended when the column names are not valid Python identifiers because this method will change
the no valid identifiers following these rules:
* If the field name has a character that is not valid as Python identifier, it will be replaced by _.
* If the field name starts with a number, then the character 'n' is added at the beginning.

For example, if you have the following data file in CSV:

```text
1d,D&D,Figures
20,Main dice all
...
```

The identifier for the object attributes will be __n1d__, __D_D__ and __Figures__, respectively. The last field does not
change because it is a valid Python identifier.

For this reason in these cases it is better to use the parameter __mode__, which allows to change the mode to obtain
the information in each iteration. This way, you can obtain a dictionary (__mode=ReadMode.DICT__) or a list 
(__mode=ReadMode.LIST__) instead of a Python object. For example, this sentences do the same that the previous code
does:

```python
from filedatasource import CsvReader, ReadMode

# To get a dictionary instead an objects in each iteration
with CsvReader('data.csv', mode=ReadMode.DICT) as reader:
    for person in reader:
        print(person['name'], person['surname'], person['fullname'])
        
# To get a list of values instead of an object with attributes
with CsvReader('data.csv', mode=ReadMode.LIST) as reader:
    for person in reader:
        print(person[0], person[1], person[2])
```

All these operations can be done with Excel files using __ExcelReader__. For example, to read the **data.xlsx** with
the above content you can do the following:

```python
from filedatasource import ExcelReader

with ExcelReader('data.xslx') as reader:
    for person in reader:
        print(person.name, person.surname, person.address)
```

If the file name ends with **.xls** instead of **.xlsx**, this class will read it correctly too.

Regardless of using __CsvReader__ or __ExcelReader__, you can use the __tqdm()__ method to measure the time that
you process will take. For example:

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

However, the __CsvReader__ needs, previously, to pre-read the entire file to calculate the number of rows, and it 
might take a bit longer. This problem does not occur with the Excel file because it is fully loaded into memory.

In an Excel file you can know the list of sheet names by means of sheets():

```python
from filedatasource import sheets

# It detects the type of the Excel file by the extension of the filename.
sheets('test/Example.xlsx')
sheets('test/Example.xls')
```

## How to write a data file

With **filedatasource** is very easy to write, both, a CSV file (compressed or not) and an Excel file (xls or xlsx).
Only you need to use __CsvWriter__ or __ExcelWriter__ writing the rows by parameters, with a list of values or 
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

If you in your object class defines properties, you can use it directly as __fieldnames__ parameter. For example:

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

By default, if the file 'data.csv' exists, it will be removed. In order to avoid it and add the rows at the end of the 
file, you can use the __mode__ parameter with the value __Mode.APPEND__ like this:

```python
from filedatasource import CsvWriter, Mode

# Creating a CsvWriter in APPEND mode
with CsvWriter('data.csv', fieldnames=['a', 'b', 'c'], mode=Mode.APPEND) as writer:
    writer.write_dicts([
        {'a': 10, 'b': 11, 'c': 12},
        {'a': 13, 'b': 14, 'c': 15}
    ])

from filedatasource import ExcelWriter, Mode

# Creating a ExcelWriter in APPEND mode (important note below)
with ExcelWriter('data.xlsx', fieldnames=['a', 'b', 'c'], mode=Mode.APPEND) as writer:
    writer.write_dicts([
        {'a': 10, 'b': 11, 'c': 12},
        {'a': 13, 'b': 14, 'c': 15}
    ])
```

**Important note**: If an Excel file has more than one sheet, the append mode will remove all the rest sheets.

## Working with Excel sheets

__ExcelReader__ only works with one Excel sheet at a time. You can select the sheet to read using the parameter 
__sheet__ using the sheet name or its number (starting by 0). For example, if we have the file **Example.xls** with
two sheets, the first one named **Clients**, and the second one named **Suppliers**, you can do the following:

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

With **filedatasource** you can read or write a whole data file in two lines using __DataWriter.write_lists()__,
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
All these methods also work with __ExcelWriter__.

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

## Convert from CSV to Excel and viceversa

With these tools, it is very simply to convert from a CSV to an Excel file and viceversa:

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

What's more, it can be even easier: 

```python
from filedatasource import convert

convert('data.csv', 'data.xlsx')
```
## Reading CSV with field types

In Excel files you can save information maintaining their original data types. For example, if you store a row with
different field types, you can retrieve the information with the same vale types. For instance:

```python
from filedatasource import  ExcelWriter, ExcelReader

with ExcelWriter('data.xlsx', fieldnames=['a', 'b', 'c', 'd']) as writer:
    writer.write(['One', 2, 3.0, True])
with ExcelReader('data.xlsx') as reader:
    print(reader.read_list()) # --> print ['One', 2, 3.0, True]
```

However, a CSV file does not contain any information about field types. And using CsvWriter and CsvReader in the 
same way you will get the list ['One', '2', '3.0', 'True']. That means, all the values in string format. 
To solve this, you can use the **types** parameter as following:

```python
from filedatasource import  CsvWriter, CsvReader

with CsvWriter('data.csv', fieldnames=['a', 'b', 'c', 'd']) as writer:
    writer.write(['One', 2, 3.0, True])
# Define how the data type of each field using a list
with CsvReader('data.csv', types=[str, int, float, bool]) as reader:
    print(reader.read_list()) # -> print ['One', 2, 3.0, True])
# Define how the data type of each field using a dictionary
with CsvReader('data.csv', types={'a': str, 'b': int, 'c': float, 'd': bool}) as reader:
    print(reader.read_list()) # -> print ['One', 2, 3.0, True])
```

This way, you can define the data values in the correct field type. If there are fields without defining, then 
a string value will be returned for those fields.

## Writers with predefined fieldnames

If you are using the same writer several times, you can use a subclass in order to avoid define the __fieldnames__ 
several times overwriting the fieldnames property. For example:

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

However, it could be easier using just one line using the functions __load()__ and  __save()__, 
__save_dicts()__ or __save_lists()__. This method load and/or save Excel or CSV files based on the file extension.

```python
from filedatasource import load, save, save_dicts, save_lists, ReadMode

# Obtain a list of objects from a CSV file and print the first row.
objs = load('data.csv')
print(objs[0].a, objs[0].b, objs[0].c)

# Obtain a list of dictionaries from a compressed CSV file and print the first row.
dicts = load('data.csv.gz', mode=ReadMode.DICT)
print(dicts[0]['a'], dicts[0]['b'], dicts[0]['c'])

# Obtain a list of lists from an Excel file and print the first row.
lists = load('data.xlsx', mode=ReadMode.LIST)
print(lists[0][0], lists[0][1], lists[0][2])

# Write a list of objects in a XLS file
data_objects = [
    Example(16, 17, 18),
    Example(19, 20, 21),
    Example(22, 23, 24)
]
save('data.xls', data_objects)

# Write a list of dictionaries in a XLS file
data_dict = [
    {'a': 10, 'b': 11, 'c': 12},
    {'a': 13, 'b': 14, 'c': 15}
]
save_dicts('data.xls', data_dict)

# Write a list of lists in a XLSX file with the column names 'a', 'b' and 'c'
data_list = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
save_lists('data.xlsx', data_list, fieldnames=['a', 'b', 'c'])
```

It is possible to use the function __load_objs()__, __load_dicts()__ and __load_lists()__ instead of 
the function __load()__ with the parameter __mode__.

Also, it is possible to use the functions __list2csv()__, __dict2csv()__, __objects2csv()__, __list2excel()__,
__dict2excel()__ and __objects2excel()__ in order to force the format of the output file independently of the file
extension:

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
# Write a list of objects into a compressed CSV file
objects2csv('data.csv.gz', data_objects, fieldnames=['a', 'b', 'c'])
# Write a list of lists into an Excel file
list2excel('data.xlsx', data_list, fieldnames=['a', 'b', 'c'])
# Write a list of dicts into an Excel file
dict2excel('data.xlsx', data_dict, fieldnames=['a', 'b', 'c'])
# Write a list of objects into a XLS file
objects2excel('data.xls', data_objects, fieldnames=['a', 'b', 'c'])
```

And, you can also use the equivalent functions __csv2list()__, __csv2dict()__, __csv2objects()__,
__excel2list()__, __excel2dict()__, and __excel2objects()__. For example:

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

# Read the first sheet from an Excel
with open_reader('data.xlsx') as reader:
   ...

# Write a CSV
with open_writer('data.csv', fieldnames=[...]) as writer:
    ...

# Write a compressed CSV
with open_writer('data.csv.gz', fieldnames=[...]) as writer:
    ...

# Write an Excel file creating a default sheet
with open_writer('data.xlsx', fieldnames=[...]) as writer:
   ...
```

Using the __open_reader()__ you can use the __mode__ parameter to set how get each row.

```python
from filedatasource import open_reader, ReadMode

# Reading the file and returning objects
with open_reader('data.xlsx') as reader:
   for obj in reader:
        print(obj.a, obj.b, obj.c)

# Read the file and returning dictionaries
with open_reader('data.csv', mode=ReadMode.DICT) as reader:
   for d in reader:
        print(d['a'], d['b'], d['c'])

# Read the file and returning lists of values
with open_reader('data.csv.gz', mode=ReadMode.LIST) as reader:
   for lst in reader:
        print(lst[0], lst[1], lst[2])
```

## Size calculation

It is possible to know how many rows has a data source for both, writer or reader. For example:

```python
from filedatasource import open_reader, open_writer

# How to know the number of rows in a reader with data
with open_reader('data.csv') as reader:
    print(len(reader))

# How to know the number of rows in a writer
with open_writer('data.csv', fieldnames=['a', 'b', 'c']) as writer:
    print(len(writer))  # Print 0 because the file is opened for write.
    writer.write(a=1, b=2, c=3)
    writer.write(a=4, b=5, c=6)
    print(len(writer))  # Print 2 because has been added two rows.
```

**Note**: The file length calculation does not work with readers oppened with a file stream instead of a file path or 
with a writer opened with append mode and from a file stream.
