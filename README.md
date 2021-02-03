# File data-source
Convert several file data sources (like typical CSV or Excel) to Python objects or dictionaries in an easy way.

## Install
pip install -i https://test.pypi.org/simple/ filedatasource

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

The simplest code will be:

```python
from filedatasource import CsvReader

with CsvReader('data.csv') as reader:
    for person in reader:
        print(person.name, person.surname, person.address)
```

If the file name ends with .gz then, CsvReader() will decompress during the reading.

For the **data.xlsx** file with the following content is very similar:

```text
+-----+-------+------------------------+
|name |surname|address                 |
|Jhon |Smith  |Oxford street           |
|Maria|Ortega |George Washington street|
+-----+-------+------------------------+
```

The simplest code will be:

```python
from filedatasource import ExcelReader

with ExcelReader('data.xslx') as reader:
    for person in reader:
        print(person.name, person.surname, person.address)
```

In both cases you can use tqdm():

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

Also,it is very simply to convert form a Csv to Excel and viceversa:

```python
from filedatasource import ExcelWriter, CsvReader

with CsvReader('data.csv') as reader:
    with ExcelWriter('data.xlsx', fieldnames=reader.fieldnames) as writer:
        for obj in reader:
            writer.write(obj)
```

But it can be easier: 

```python
from filedatasource import ExcelWriter, CsvReader

with CsvReader('data.csv') as reader:
    with ExcelWriter('data.xlsx', fieldnames=reader.fieldnames) as writer:
        writer.import_reader(reader)
```
