#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.1"
__date__ = "07/01/2023"

"""Class handles output of matching file search results to SQLite database.
"""

# standard imports
import sqlite3

# local imports
import pfllib.pflout as pflout


class PFLOutSqlite(pflout.PFLOutFile):
    """Class handles output of matching file search results to SQLite database."""

    def __init__(self, filePath, columnNames):
        super().__init__(filePath, columnNames)
        self._qmarks = (len(self._columnNames) * "?, ").strip(", ")
        self._insertCmd = f"INSERT INTO filelist VALUES ({self._qmarks})"

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
        self._dataSets = []

    def writeMatch(self, formattedList):
        if len(self._dataSets) < 50:
            self._dataSets.append(formattedList)
        else:
            self.executeInsert()

    def close(self):
        if len(self._dataSets) > 0:
            self.executeInsert()
        self._connection.close()

    def executeInsert(self):
        try:
            self._cursor.executemany(self._insertCmd, self._dataSets)
            self._connection.commit()
        except Exception as e:
            # ignore invalid data
            print(e)
            # pass
        self._dataSets = []
