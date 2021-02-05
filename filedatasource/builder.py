from typing import Union, List

from filedatasource import CsvReader, ExcelReader, CsvWriter, ExcelWriter


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
