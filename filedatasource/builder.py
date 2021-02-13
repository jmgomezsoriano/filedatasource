from typing import Union, List, TextIO, BinaryIO, Any, Dict

from filedatasource import CsvReader, ExcelReader, CsvWriter, ExcelWriter, Mode, ReadMode


def open_reader(fname: str) -> Union[CsvReader, ExcelReader]:
    """ Create a CsvReader or a ExcelReader with the parameters by default only from the file path and the extension
    of the file name. If it ends with .csv.gz or .gz, then a CSV file is created, however, if the extension
    is .xls or .xlsx, then an Excel file is read.

    :param fname: The path to the Excel or CSV file.
    :return: A CsvReader or a ExcelReader depending on the file extension.
    """
    if fname.endswith('.csv') or fname.endswith('.csv.gz'):
        return CsvReader(fname)
    if fname.endswith('.xls') or fname.endswith('.xlsx'):
        return ExcelReader(fname)
    raise ValueError(f'The file name {fname} has to finish in .csv, .csv.gz, .xls, or .xlsx to use this function')


def open_writer(fname: str, fieldnames: List[str]) -> Union[CsvWriter, ExcelWriter]:
    """ Create a CsvWriter or a ExcelWriter with the parameters by default only from the file path with a given
     extension, and the fieldnames. If the file extension ends with .csv.gz or .gz, then a CSV file is created,
     however, if the extension is .xls or .xlsx, then an Excel file is created.

    :param fname: The path to the Excel or CSV file.
    :param fieldnames: The name of the fields.
    :return: A CsvWriter or a ExcelWriter depending on the file extension.
    """
    if fname.endswith('.csv') or fname.endswith('.csv.gz'):
        return CsvWriter(fname, fieldnames=fieldnames)
    if fname.endswith('.xls') or fname.endswith('.xlsx'):
        return ExcelWriter(fname, fieldnames=fieldnames)
    raise ValueError(f'The file name {fname} has to finish in .csv, .csv.gz, .xls, or .xlsx to use this function')


def list2csv(file_or_io: Union[str, TextIO, BinaryIO], data: List[List[Any]],
             fieldnames: Union[List[str], type, object] = None,
             mode: Mode = Mode.WRITE, encoding: str = 'utf-8') -> None:
    """ Write a sequences of lists as a sequence of rows in a CSV file.

    :param file_or_io: The file path or an opened stream to use. If it is a file path and it ends in .gz, then
    :param data: The sequence of rows as lists.
    :param fieldnames: The field names of this CSV.
    :param mode: The writing mode: Mode.APPEND or Mode.WRITE. By default Mode.WRITE.
    :param encoding: The encoding (it is only used if the parameter file_or_io is a file path).
    """
    with CsvWriter(file_or_io, fieldnames, mode, encoding) as writer:
        writer.write_lists(data)


def dict2csv(file_or_io: Union[str, TextIO, BinaryIO], data: List[Dict],
             fieldnames: Union[List[str], type, object] = None,
             mode: Mode = Mode.WRITE, encoding: str = 'utf-8') -> None:
    """ Write a list of dictionaries in a CSV file.

    :param file_or_io: The file path or an opened stream to use. If it is a file path and it ends in .gz, then
        a compressed file is created using gzip.
    :param data: The list of dictionaries. Each dictionary has to contain as keys the fieldnames and as value
        the row data to store.
    :param fieldnames: The field names of this CSV.
    :param mode: The writing mode: Mode.APPEND or Mode.WRITE. By default Mode.WRITE.
    :param encoding: The encoding (it is only used if the parameter file_or_io is a file path).
    """
    with CsvWriter(file_or_io, fieldnames, mode, encoding) as writer:
        writer.write_dicts(data)


def objects2csv(file_or_io: Union[str, TextIO, BinaryIO], data: List[object],
                fieldnames: Union[List[str], type, object] = None,
                mode: Mode = Mode.WRITE, encoding: str = 'utf-8') -> None:
    """ Write a sequence of objects in a CSV file.

    :param file_or_io: The file path or an opened stream to use. If it is a file path and it ends in .gz, then
        a compressed file is created using gzip.
    :param data: The sequence of objects to write with public attributes or properties.
    :param fieldnames: The field names of this CSV.
    :param mode: The writing mode: Mode.APPEND or Mode.WRITE. By default Mode.WRITE.
    :param encoding: The encoding (it is only used if the parameter file_or_io is a file path).
    """
    with CsvWriter(file_or_io, fieldnames, mode, encoding) as writer:
        writer.write_objects(data)


def list2excel(fname: str, data: List[List[Any]], sheet: Union[str, int] = 0,
               fieldnames: Union[List[str], type, object] = None) -> None:
    """ Write a sequences of lists as a sequence of rows in an Excel file.

    :param fname: The file path to the Excel file.
    :param data: The sequence of rows as lists.
    :param sheet: The sheet to write.
    :param fieldnames: The list of fieldnames. It could be given as a list or a type or object with properties or
    attributes.
    """
    with ExcelWriter(fname, sheet, fieldnames) as writer:
        writer.write_lists(data)


def dict2excel(fname: str, data: List[Dict], sheet: Union[str, int] = 0,
               fieldnames: Union[List[str], type, object] = None) -> None:
    """ Write a list of dictionaries in an Excel file.

    :param fname: The file path to the Excel file.
    :param data: The list of dictionaries. Each dictionary has to contain as keys the fieldnames and as value
        the row data to store.
    :param sheet: The sheet to write.
    :param fieldnames: The list of fieldnames. It could be given as a list or a type or object with properties or
    attributes.
    """
    with ExcelWriter(fname, sheet, fieldnames) as writer:
        writer.write_dicts(data)


def objects2excel(fname: str, data: List[object], sheet: Union[str, int] = 0,
                  fieldnames: Union[List[str], type, object] = None) -> None:
    """ Write a sequence of objects in an Excel file.

    :param fname: The file path to the Excel file.
    :param data: The sequence of objects to write with public attributes or properties.
    :param sheet: The sheet to write.
    :param fieldnames: The list of fieldnames. It could be given as a list or a type or object with properties or
    attributes.
    """
    with ExcelWriter(fname, fieldnames, sheet) as writer:
        writer.write_objects(data)


def csv2list(file_or_io: Union[str, TextIO, BinaryIO], encoding: str = 'utf-8') -> List[List[Any]]:
    """ Read a CSV file (compressed or not) and return a list of lists with the file rows.

    :param file_or_io: The file path or the file stream.
    :param encoding: The file encoding.
    :return: A List of lists with the file rows. Each column value is stored as list element.
    """
    with CsvReader(file_or_io, ReadMode.LIST, encoding) as reader:
        return reader.read_lists()


def csv2dict(file_or_io: Union[str, TextIO, BinaryIO], encoding: str = 'utf-8') -> List[Dict]:
    """ Read a CSV file (compressed or not) and return a list of dictionaries with the file content..

    :param file_or_io: The file path or the file stream.
    :param encoding: The file encoding.
    :return: A list of dictionaries. Each dictionary represents a row and it contains as keys the column name and
    its value the column value.
    """
    with CsvReader(file_or_io, ReadMode.DICT, encoding) as reader:
        return reader.read_rows()


def csv2objects(file_or_io: Union[str, TextIO, BinaryIO], encoding: str = 'utf-8') -> List[object]:
    """ Read a CSV file (compressed or not) and return a list of objects.

    :param file_or_io: The file path or the file stream.
    :param encoding: The file encoding.
    :return: A list of objects. Each object is a file row with the attributes as column names and its value.
    """
    with CsvReader(file_or_io, ReadMode.OBJECT, encoding) as reader:
        return reader.read_objects()


def excel2list(fname: str, sheet: Union[str, int] = 0) -> List[List[Any]]:
    """ Read a Excel file (xlsx or xls) and return a list of lists with the file rows.

    :param fname: The file path to the Excel file..
    :param sheet: The sheet name or the sheet number (starting by 0).
    :return: A List of lists with the file rows. Each column value is stored as list element.
    """
    with ExcelReader(fname, sheet, ReadMode.LIST) as reader:
        return reader.read_lists()


def excel2dict(fname: str, sheet: Union[str, int] = 0) -> List[Dict]:
    """ Read a Excel file (xlsx or xls) and return a list of dictionaries with the file content..

    :param fname: The file path to the Excel file.
    :param sheet: The sheet name or the sheet number (starting by 0).
    :return: A list of dictionaries. Each dictionary represents a row and it contains as keys the column name and
    its value the column value.
    """
    with ExcelReader(fname, sheet, ReadMode.DICT) as reader:
        return reader.read_rows()


def excel2objects(fname: str, sheet: Union[str, int] = 0) -> List[object]:
    """ Read a Excel file (xlsx or xls) and return a list of objects.

    :param fname: The file path to the Excel file.
    :param sheet: The sheet name or the sheet number (starting by 0).
    :return: A list of objects. Each object is a file row with the attributes as column names and its value.
    """
    with ExcelReader(fname, sheet, ReadMode.OBJECT) as reader:
        return reader.read_objects()
