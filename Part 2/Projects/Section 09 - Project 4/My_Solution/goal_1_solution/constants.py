"""This is the config file."""

from parse_utils import parse_date


# Files
fname_personal = "data/personal_info.csv"
fname_employment = "data/employment.csv"
fname_vehicles = "data/vehicles.csv"
fname_update_status = "data/update_status.csv"

fnames = fname_personal, fname_employment, fname_vehicles, fname_update_status

# Parsers (what parser func do we want to use on each file? Note: `str` is a function)
personal_parser = (str, str, str, str, str)  # we want all 5 columns to be str for this file
employment_parser = (str, str, str, str)  # we want all 4 columns to be str for this file
vehicle_parser = (str, str, str, int)
update_status_parser = (str, parse_date, parse_date)

parsers = personal_parser, employment_parser, vehicle_parser, update_status_parser

# Names for the NamedTuples. Each row of data is a namedtuple where their name is the file that the row comes from
personal_class_name = 'Personal'
employment_class_name = 'Employment'
vehicle_class_name = 'Vehicle'
update_status_class_name = 'UpdateStatus'

class_names = personal_class_name, employment_class_name, vehicle_class_name, update_status_class_name