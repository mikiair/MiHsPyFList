#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.1"
__date__ = "06/30/2023"

"""Class handle output of file list results to SQLite database
"""

# standard imports
import sqlite3

# local imports
import pfllib.pflout as pflout


class PFLOutSqlite(pflout.PFLOut):
    def __init__(self, filePath, columnNames, showdots):
        self._filePath = filePath
        self._columnNames = columnNames
        self._qmarks = (len(self._columnNames) * "?, ").strip(", ")
        self._insertCmd = f"INSERT INTO filelist VALUES ({self._qmarks})"
        self._showDots = showdots

    def openout(self, mode):
        self._connection = sqlite3.connect(self._filePath)  # , mode, newline="")
        self._cursor = self._connection.cursor()
        if mode == "w":
            try:
                sqlCmd = "DROP TABLE filelist"
                self._cursor.execute(sqlCmd)
                self._connection.commit()
            except Exception:
                pass

        joinedCols = (", ".join(self._columnNames)).strip(", ")
        sqlCmd = f"CREATE TABLE filelist({joinedCols})"
        self._cursor.execute(sqlCmd)
        self._connection.commit()

    def writeMatch(self, formattedList):
        try:
            self._cursor.execute(self._insertCmd, formattedList)
            self._connection.commit()
        except Exception as e:
            # ignore invalid data
            print(e)
            # pass
        if self._showDots:
            print(".", end="")

    def close(self):
        self._connection.close()
        if self._showDots:
            print("")
