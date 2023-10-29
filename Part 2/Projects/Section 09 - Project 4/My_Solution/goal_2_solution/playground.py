import constants
import parse_utils
import itertools

# # see a sample of what is in each file
# for fname in constants.fnames:
#     print(fname)
#     with open(fname) as f:
#         print(next(f), end="")
#         print(next(f), end="")
#         print(next(f), end="")
#     print()

# # try out the csv reader
# for fname in constants.fnames:
#     print(fname)
#     with open(fname) as f:
#         reader = csv.reader(f, delimiter=",", quotechar='"')
#         print(next(reader))
#         print(next(reader))
#     print()

# # use our parse utils to get header row only.
# for fname in constants.fnames:
#     print(fname)
#     reader = parse_utils.csv_parser(fname, include_header=True)
#     print(next(reader), end='\n')


# # use our parse utils to get just the data.
# for fname in constants.fnames:
#     print(fname)
#     reader = parse_utils.csv_parser(fname)
#     print(next(reader), end='\n')

# # try out date parser
# reader = parse_utils.csv_parser(constants.fname_update_status)
# for _ in range(3):
#     record = next(reader)
#     print(record[0], record[1], type(parse_utils.parse_date(record[1])))

# # try out iter_file
# for fname, class_name, parser in zip(constants.fnames, constants.class_names, constants.parsers):
#     file_iter = parse_utils.iter_file(fname, class_name, parser)
#     print(fname)
#     for _ in range(3):
#         print(next(file_iter))
#     print()


# parse_utils.iter_combined_plain_tuple(
#     constants.fnames, constants.class_names, constants.parsers, constants.compress_fields
# )

# # try create_combo_named_tuple_class function
# nt = parse_utils.create_combo_named_tuple_class(constants.fnames, constants.compress_fields)
# print(nt._fields)

data_iter = parse_utils.iter_combined(
    constants.fnames, constants.class_names, constants.parsers, constants.compress_fields
)
for row in itertools.islice(data_iter, 5):
    print(row)
