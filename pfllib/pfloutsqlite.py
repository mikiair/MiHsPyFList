#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.1.1"
__date__ = "07/14/2023"

"""Class handles output of matching file search results to SQLite database.
"""

# local imports
import pfllib.pflout as pflout
import pfllib.pfsql as pfsql


class PFLOutSqlite(pflout.PFLOutFile):
    """Class handles output of matching file search results to SQLite database."""

    def __init__(self, filePath, columnNames, basePath):
        super().__init__(filePath, columnNames)
        self._db = None
        self._basePath = str(basePath).rstrip("\\")
        self._basePathLen = len(self._basePath)

        self._qmarks = (len(self._columnNames) * "?, ").strip(", ")
        self._insertCmd = f"INSERT INTO filelist VALUES ({self._qmarks})"

    def openout(self, mode):
        self._db = pfsql.opendb(self._filePath)
        if mode == "w":
            try:
                pfsql.droptable(self._db, "filelist")
                pfsql.droptable(self._db, "dirlist")
            except Exception:
                pass

        pfsql.createtable(self._db, "dirlist", ["id INTEGER PRIMARY KEY", "path"])
        self._currentPathID = self.insertPath(self._basePath)
        self._currentPath = None

        self._columnNames[0] += " REFERENCES dirlist(id)"
        pfsql.createtable(self._db, "filelist", self._columnNames)
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

    def flushMatches(self):
        if len(self._dataSets) > 0:
            self.executeInsertFiles()

    def close(self):
        if self._db is not None:
            pfsql.closedb(self._db)

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
