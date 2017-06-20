"""Module to hold the functionality for storing sensor data."""

import logging
import sqlite3
import os
from utils import senstat_paths, table_name, db_name
import pandas as pd


data_store_logger = logging.getLogger(__file__)
data_store_logger.setLevel(logging.INFO)


def get_db_connection():
    """Get a connection to the database."""

    # Get a path pointing at the database
    db_path = os.path.join(senstat_paths['data'], db_name)

    db_conn = sqlite3.connect(db_path)

    return db_conn


def get_table_cursor(db_conn):
    """Get a cursor to a database connection."""

    cursor = db_conn.cursor()

    # Check to see if the table exists, and create if not
    cursor.execute("""SELECT ? FROM sqlite_master WHERE type='table';""",
                   (table_name, ))

    # Create the table if it doesn't already exist
    if not cursor.fetchall():
        data_store_logger.info("No instance of table {} exists, creating table".
                               format(table_name))
        exe_str = "CREATE TABLE " + table_name + "(date text, temperature real)"
        cursor.execute(exe_str)
        db_conn.commit()

    return cursor


def write_table_entry(db, cursor, time_str, temp):
    """Write an entry to the table."""
    exe_str = "INSERT INTO " + table_name + " VALUES (?, ?);"
    cursor.execute(exe_str, (time_str, temp,))
    db.commit()


def read_into_df():
    """Read the entire table into a pandas dataframe."""
    db = get_db_connection()
    sql = "SELECT * FROM " + table_name
    df = pd.read_sql(sql, db)
    db.close()
    return df


def show_recent():
    """Show recent entries to the database."""
    df = read_into_df()
    print(df.tail())


if __name__ == "__main__":
    show_recent()