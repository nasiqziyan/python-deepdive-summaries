import csv
from datetime import datetime
from collections import namedtuple


def csv_parser(fname, *, delimiter=",", quotechar='"', include_header=False):
    with open(fname) as f:
        reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)

        if not include_header:
            next(f)  # This is slightly better than next(reader) because reader
            #          hasn't actually opened up the data.So, this version
            #          skips the actual parsing of the first row.
        yield from reader


def parse_date(value, *, fmt="%Y-%m-%dT%H:%M:%SZ"):
    return datetime.strptime(value, fmt)


def extract_field_names(fname):
    reader = csv_parser(fname, include_header=True)
    return next(reader)


def create_named_tuple_class(fname, class_name):
    """
    Creates a namedtuple whose field names correspond to the column headings 
    in the file that it comes from.
    """
    fields = extract_field_names(fname)
    return namedtuple(class_name, fields)


def iter_file(fname, class_name, parser):
    """
    Iterates through a file converting each row into a named tuple
    whose name (class_name) is the file that it comes from.
    """
    nt_class = create_named_tuple_class(fname, class_name)
    reader = csv_parser(fname)
    for row in reader:
        parsed_data = (parse_fn(value) for value, parse_fn in zip(row, parser)) 
        yield nt_class(*parsed_data)
