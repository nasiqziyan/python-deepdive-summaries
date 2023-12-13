import constants
import parse_utils
import itertools
from datetime import datetime

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

# ------------- GOAL 3 ---------------

print('------------ ACTUAL SOLUTION FOR GOAL 3 --------------')

cutoff_date = datetime(2018, 3, 1)
filtered_iter = parse_utils.filter_iter_combined(constants.fnames, constants.class_names, constants.parsers,
                                                 constants.compress_fields,
                                                 key=lambda row: row.last_updated >= cutoff_date)
for row in filtered_iter:
    print(row)

# ------------- GOAL 4 ---------------

print('-------------------------------')

cutoff_date = datetime(2017, 3, 1)

# ----------------- FIRST APPROACH VIA GROUPBY: START ----------------------

# def group_key(item):
#     return item.gender, item.vehicle_make
#
# data = parse_utils.filter_iter_combined(constants.fnames, constants.class_names, constants.parsers,
#                                                  constants.compress_fields,
#                                                  key=lambda row: row.last_updated >= cutoff_date)

# # `itertools.groupby requires sorted data`.
# # We can sort by two keys; the first key will ensure that ALL the females are first and then ALL the males.
# # Then, out of all the females, they will be rearranged based on vehicles - and similarly for the males.
# sorted_data = sorted(data, key=group_key)
#
# # `groupby` produces an iterator of tuples. Each tuple contains a key and a subiterator
# # `groupby` -> ((<key_1>, <subiter_1>), (<key_2>, <subiter_2>), (<key_3>, <subiter_3>))
# # Since our key contained a tuple of two, so will our key in the `groupby` object:
# # `groupby` -> (
# #                (('Female', 'Acura'), <subiter_1>),
# #                (('Female', 'Aston Martin'), <subiter_2>),
# #                (('...', '...'), <...>),
# #                (('Male', 'Acura'), <subiter_100>)
# #                (('Male', 'Aston'), <subiter_101>)
# #              )
#
# # Use the following to view the above and also consume the subiters.
# groups = itertools.groupby(sorted_data, key=group_key)
# for key, group in groups:
#     print(key)
#     for item in group:
#         print(item)
#     print('-----------------------------------------')

# ----------------- FIRST APPROACH VIA GROUPBY: END ----------------------

# ----------------- SECOND APPROACH VIA DATA SPLIT: START ----------------------


# We are not going to use the above approach of sorting the entire data and
# then creating two groupby's for the entire dataset. Instead, we'll split the
# data into male and female and then filter each separately which is much simpler and efficient.

# data = parse_utils.filter_iter_combined(constants.fnames, constants.class_names, constants.parsers,
#                                                  constants.compress_fields,
#                                                  key=lambda row: row.last_updated >= cutoff_date)
#
# # We don't have to worry about `tee` being shallow copy here because `data` doesn't contain any subiterators.
# data_1, data_2 = itertools.tee(data, 2)
#
# print("GROUPS_M")
# data_m = (row for row in data_1 if row.gender == "Male")
# sorted_data_m = sorted(data_m, key=lambda row: row.vehicle_make)
# groups_m = itertools.groupby(sorted_data_m, key=lambda row: row.vehicle_make)
# group_m_counts = ((group[0], len(list(group[1]))) for group in groups_m)
# for row in group_m_counts:
#     print(row)
#
# print("\n")
# print("GROUPS_F")
# data_f = (row for row in data_2 if row.gender == "Female")
# sorted_data_f = sorted(data_f, key=lambda row: row.vehicle_make)
# groups_f = itertools.groupby(sorted_data_f, key=lambda row: row.vehicle_make)
# group_f_counts = ((group[0], len(list(group[1]))) for group in groups_f)
# for row in group_f_counts:
#     print(row)

# ----------------- SECOND APPROACH VIA DATA SPLIT: END ----------------------

# Since we know it works, and we notice lots of repeated code, let's refactor it in parse_utils.

cutoff_date = datetime(2017, 3, 1)

results_f = parse_utils.group_data(constants.fnames, constants.class_names, constants.parsers,
                                   constants.compress_fields,
                                   filter_key=lambda row: row.last_updated >= cutoff_date and row.gender == "Female",
                                   group_key=lambda row: row.vehicle_make)

print("RESULTS_F")
for row in results_f:
    print(row)

results_m = parse_utils.group_data(constants.fnames, constants.class_names, constants.parsers,
                                   constants.compress_fields,
                                   filter_key=lambda row: row.last_updated >= cutoff_date and row.gender == "Male",
                                   group_key=lambda row: row.vehicle_make)

print("\nRESULTS_M")
for row in results_m:
    print(row)
