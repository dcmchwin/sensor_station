"""Utilities for general use in sensor station project."""

from os.path import dirname, join

def get_paths():
    """Return a dictionary of useful paths."""

    py_dir = dirname(__file__)
    root_dir = dirname(py_dir)
    data_dir = join(root_dir, 'data')

    senstat_paths = {}

    senstat_paths['python'] = py_dir
    senstat_paths['root'] = root_dir
    senstat_paths['data'] = data_dir

    return senstat_paths

senstat_paths = get_paths()
"""
Get paths for project which are generally useful.
"""

db_name = "home_climate.db"
"""
Get the database name to store home climate data in.
"""

table_name = 'climate'
"""
Get the table name within the database that stores climate data.
"""

time_format = "%Y-%m-%dT%H:%M:%S%z"
"""
Get a ISO 8601 compatible datetime format.
"""