import csv
from datetime import datetime
from collections import namedtuple
import itertools


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


def create_combo_named_tuple_class(fnames, compress_fields):
    """
    Create a combo namedtuple whose field names correspond to the *desired* column headings
    in the file that it comes from. The *desired* column headings are found in
    `compress_fields`.
    """

    compress_fields = itertools.chain(*compress_fields)
    combo_field_names = (extract_field_names(fname) for fname in fnames)
    # next(combo_field_names) -> (('ssn', 'name', 'age'), ('ssn', 'role', 'salary'), ('ssn', 'car', 'make'))
    # We want to "unpack" these 3 tuples into one single tuple -> use itertools.chain!
    field_names = itertools.chain(*combo_field_names)
    # -> ('ssn', 'name', 'age','ssn', 'role', 'salary', 'ssn', 'car', 'make')
    comprssed_field_names = itertools.compress(field_names, compress_fields)
    # -> ('name', 'age', 'role', 'salary', 'car', 'make')
    return namedtuple("Data", comprssed_field_names)


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


# def playground_iter_combined_plain_tuple(fnames, class_names, parsers, compress_fields):
#     """
#     THIS FUNCTION IS TO UNDERSTAND THE COMPONENTS OF THE REAL ITER_COMBINED_PLAIN_TUPLE_FUNCTION
#     THE REAL ONE IS BELOW
#     We want to apply `iter_file` onto each file to produce a tuple and then combine
#     the fields of all the tuples into one super tuple. But, the problem is `iter_file`
#     produces a single tuple of numerous fields. We need to make sure that we don't
#     create a tuple of tuples e.g.
#     (  file_a_tuple(...), file_b_tuple(...), file_c_tuple(...), file_d_tuple(...)  ).
#     The solution is to unpack each file tuple into the super tuple.

#     As tuples are immutable, you cannot do this without itertools.chain. Try if you don't
#     believe me.
#     """
#     tuples = [iter_file(fname, class_name, parser) for fname, class_name, parser in zip(fnames, class_names, parsers)]
#     # tuples is a list of 4 generators, each one corresponding to a different csv file in our data folder.
#     # -> [
#           (Person(name='a', age=1), Person(name='b', age=2), ...),
#           (Employment(role='A', salary=1), Employment(role='B', salary=2), ...),
#           (Vehicle(car='A', make='A'), Vehicle(car='B', make='B'), ...)
#          ]

#     zipped_tuples = zip(*tuples)
# we can now generate the first item from each generator
#     # next(zipped_tuples) -> (Person(name='a', age=1), Employment(role='A', salary=1), Vehicle(car='A', make='A'))
#     # next(zipped_tuples) -> (Person(name='b', age=2), Employment(role='B', salary=2), Vehicle(car='B', make='B'))

#     for zipped_tuple in zipped_tuples:
#         # zipped_tuple -> (Person(name='a', age=1), Employment(role='A', salary=1), Vehicle(car='A', make='A'))
#         print(list(itertools.chain(*zipped_tuple)))
#         # itertools.chain(*zipped_tuple) -> ('a', 1, 'A', 1, 'A', 'A'); this is what we want, but we need the field names
#         # In my simplified example above we have 3 named tuples, each with 2 fields.
#         # We would also have 3 compress lists, each containing 2 values.
#         # Now that we have combined the 3 tuples into a single tuple of 6 values, we can also
#         # combine our 3 compress lists into a single list of 6 values.
#         # In our real case, we will actually get a single list of 19 values.
#         print()
#         print()
#         break


def iter_combined_plain_tuple(fnames, class_names, parsers, compress_fields):
    # WE DON'T USE THIS AS OUR FINAL EITHER; WE USE `iter_combined`.
    # We need to make a list out of compress_fields because, otherwise it will become exhausted
    # by the 2nd iteration of `for row in merged iter`! To elaborate, inside itertools.compress in that loop,
    # we use `row` once (before moving onto the next) but we use the same `compress_fields` in every
    # iteration of the loop.
    compress_fields = list[itertools.chain(*compress_fields)]
    tuples = [iter_file(fname, class_name, parser) for fname, class_name, parser in zip(fnames, class_names, parsers)]

    zipped_tuples = zip(*tuples)

    merged_iter = (itertools.chain(*zipped_tuple) for zipped_tuple in zipped_tuples)
    # This generator expression can generate several thousand objects. Each object is an itertools.chain object.
    # If we `list(itertools.chain_object)` for a given generated object,
    # we will get a list of 19 objects corresponding to the 19 total fields across all files.
    for row in merged_iter:
        compressed_row = itertools.compress(row, *compress_fields)
        yield compressed_row


def iter_combined(fnames, class_names, parsers, compress_fields):
    combo_nt = create_combo_named_tuple_class(fnames, compress_fields)
    # We need to make a list out of compress_fields because, otherwise it will become exhausted
    # by the 2nd iteration of `for row in merged iter`! To elaborate, inside itertools.compress in that loop,
    # we use `row` once (before moving onto the next) but we use the same `compress_fields` in every
    # iteration of the loop.
    compress_fields = list(itertools.chain(*compress_fields))
    tuples = [iter_file(fname, class_name, parser) for fname, class_name, parser in zip(fnames, class_names, parsers)]
    zipped_tuples = zip(*tuples)

    merged_iter = (itertools.chain(*zipped_tuple) for zipped_tuple in zipped_tuples)
    # This generator expression can generate several thousand objects. Each object is an itertools.chain object.
    # If we `list(itertools.chain_object)` for a given generated object,
    # we will get a list of 19 objects corresponding to the 19 total fields across all files.
    for row in merged_iter:
        compressed_row = itertools.compress(row, compress_fields)
        yield combo_nt(*compressed_row)

# ------------- GOAL 3 ---------------

def filter_iter_combined(fnames, class_names, parsers, compress_fields, *, key=None):
    iter_combo = iter_combined(fnames, class_names, parsers, compress_fields)
    yield from filter(key, iter_combo)

# ------------- GOAL 4 ---------------

def group_data(fnames, class_names, parsers, compress_fields, filter_key, group_key):

    data = filter_iter_combined(fnames, class_names, parsers, compress_fields,
                                                     key=filter_key)

    sorted_data = sorted(data, key=group_key)
    groups = itertools.groupby(sorted_data, key=group_key)
    group_counts = ((group[0], len(list(group[1]))) for group in groups)
    return sorted(group_counts, key=lambda row:row[1], reverse=True)