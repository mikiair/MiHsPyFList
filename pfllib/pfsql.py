#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.2"
__date__ = "07/15/2023"

"""Module with SQLite helper functions (copied from MiHsPyFSync/pfslib).
"""

# standard imports
import sqlite3


def opendb(dbFileName):
    """Open a SQLite database file and return a tuple with connection and cursor object."""
    connection = sqlite3.connect(dbFileName)
    cursor = connection.cursor()
    return (connection, cursor)


def tableexists(db, tableName):
    """Return true if tablename exists in the database."""
    selectCmd = (
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}'"
    )
    return db[1].execute(selectCmd) is not None


def createtable(db, newTable, columnNames, ifnotexists=False):
    """Create a new table with specified columns for a database referenced by a
    tuple db = (connection, cursor), optionally create if not yet existing.
    """
    joinedCols = (", ".join(columnNames)).strip(", ")
    if not ifnotexists:
        sqlCmd = f"CREATE TABLE {newTable}({joinedCols})"
    else:
        sqlCmd = f"CREATE TABLE IF NOT EXISTS {newTable}({joinedCols})"
    db[1].execute(sqlCmd)
    db[0].commit()


def droptable(db, tableName, ifexists=False):
    """Delete a table from the database referenced by the tuple db = (connection, cursor)."""
    if ifexists:
        sqlCmd = f"DROP TABLE IF EXISTS {tableName}"
    else:
        sqlCmd = f"DROP TABLE {tableName}"
    db[1].execute(sqlCmd)
    db[0].commit()


def gettablecolnum(db, tablename):
    """Return the number of columns in the table."""
    selectCmd = f"SELECT COUNT(*) FROM pragma_table_info('{tablename}')"
    return db[1].execute(selectCmd).fetchone()[0]


def gettablecolnames(db, tablename):
    """Return a list with column names of that table."""
    selectCmd = f"SELECT name FROM pragma_table_info('{tablename}')"
    res = db[1].execute(selectCmd).fetchall()
    return [colname for colname, in res]


def insertrow(db, tablename, parampattern, params):
    """Insert a row into a table with the given values."""
    insertCmd = f"INSERT INTO {tablename} VALUES ({parampattern})"
    db[1].execute(insertCmd, params)
    db[0].commit()


def insertidrow(db, tablename, parampattern, params):
    """Insert a row into a table with the given values and return the last row ID."""
    insertrow(db, tablename, parampattern, params)
    return db[1].lastrowid


def updaterow(db, tablename, columnpattern, condition, params):
    """Update columns in an existing row identified by a condition clause
    with new values.
    """
    updateCmd = f"UPDATE {tablename} SET {columnpattern} WHERE {condition}"
    db[1].execute(updateCmd, params)
    db[0].commit()


def closedb(db):
    """Close the database connection."""
    db[0].close()
