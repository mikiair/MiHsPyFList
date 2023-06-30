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
import pfllib.PFLOut as PFLOut


class PFLOutSqlite(PFLOut):
    def __init__(self, filePath, colheader, showdots):
        self._filePath = filePath
        self._colheader = colheader
        self._showDots = showdots

    def openout(self, mode):
        self._connection = sqlite3.connect(self._filePath)  # , mode, newline="")
        self._cursor = self._connection.cursor()
        self._cursor.execute("CREATE TABLE filelist(colheader)")

    def writeMatch(self, outputColumns):
        try:
            self._cursor.execute("INSERT INTO filelist VALUES " + "(*)", outputColumns)
            self._cursor.commit()
        except Exception:
            # ignore invalid data
            pass
        if self._showDots:
            print(".", end="")

    def close(self):
        self._connection.close()
        if self._showDots:
            print("")
