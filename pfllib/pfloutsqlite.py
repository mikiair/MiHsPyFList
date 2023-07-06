#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.3"
__date__ = "07/06/2023"

"""Class handles output of matching file search results to SQLite database.
"""

# standard imports
import sqlite3

# local imports
import pfllib.pflout as pflout


class PFLOutSqlite(pflout.PFLOutFile):
    """Class handles output of matching file search results to SQLite database."""

    def __init__(self, filePath, columnNames, basePath):
        super().__init__(filePath, columnNames)
        self._basePath = str(basePath)
        self._basePathLen = len(self._basePath)
        self._qmarks = (len(self._columnNames) * "?, ").strip(", ")
        self._insertCmd = f"INSERT INTO filelist VALUES ({self._qmarks})"

    def openout(self, mode):
        connection = sqlite3.connect(self._filePath)
        cursor = connection.cursor()
        self._db = (connection, cursor)
        if mode == "w":
            self.droptable("filelist")
            self.droptable("dirlist")

        self.createtable("dirlist", ["id INTEGER PRIMARY KEY", "path"])
        self._currentPathID = self.insertPath(self._basePath)
        self._currentPath = None

        self._columnNames[0] += " REFERENCES dirlist(id)"
        self.createtable("filelist", self._columnNames)
        self._dataSets = []

    def writeMatch(self, formattedList):
        if not formattedList[0] == self._currentPath:
            self._currentPathID = self.insertPath(
                str(formattedList[0])[self._basePathLen + 1 :]
            )
            self._currentPath = formattedList[0]

        formattedList[0] = self._currentPathID
        self._dataSets.append(formattedList)

        if len(self._dataSets) == 50:
            self.executeInsertFiles()

    def close(self):
        if len(self._dataSets) > 0:
            self.executeInsertFiles()
        self._db[0].close()

    def droptable(self, tableName):
        try:
            sqlCmd = f"DROP TABLE {tableName}"
            self._db[1].execute(sqlCmd)
            self._db[0].commit()
        except Exception:
            pass

    def createtable(self, tableName, columnNames):
        joinedCols = (", ".join(columnNames)).strip(", ")
        sqlCmd = f"CREATE TABLE {tableName}({joinedCols})"
        self._db[1].execute(sqlCmd)
        self._db[0].commit()

    def insertPath(self, newPath):
        """Insert a new path entry into the dirlist table."""
        insertPathCmd = "INSERT INTO dirlist VALUES (?, ?)"
        self._db[1].execute(insertPathCmd, (None, newPath))
        self._db[0].commit()
        queryPathIdCmd = "SELECT id FROM dirlist WHERE path = ?"
        newrow = self._db[1].execute(queryPathIdCmd, (str(newPath),))
        return newrow.fetchone()[0]

    def executeInsertFiles(self):
        """Insert collection with new file datasets into table."""
        try:
            self._db[1].executemany(self._insertCmd, self._dataSets)
            self._db[0].commit()
        except Exception as e:
            # ignore invalid data
            print(e)
            # pass
        self._dataSets = []
