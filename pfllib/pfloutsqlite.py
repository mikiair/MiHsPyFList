#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.2.1"
__date__ = "07/16/2023"

"""Class handles output of matching file search results to SQLite database.
"""

# standard imports
from datetime import datetime

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

        self._columnNames.append("status")
        self._pqmarks = "=?, ".join(self._columnNames) + "=?"
        self._updateCmd = f"UPDATE filelist SET {self._pqmarks} WHERE id=?"

        self._columnNames.append("id")
        self._qmarks = (len(self._columnNames) * "?, ").strip(", ")
        self._insertCmd = f"INSERT INTO filelist VALUES ({self._qmarks})"

    def openout(self, mode):
        """Open the SQLite database file and set up the required tables."""
        self._db = pfsql.opendb(self._filePath)

        if mode == "w":
            self.droptables()

        self.setuptables()

        self._currentPath = None
        self._dataSets = []

    def droptables(self):
        try:
            pfsql.droptable(self._db, "stats", True)
            # drop filelist table first as it references dirlist
            pfsql.droptable(self._db, "filelist", True)
            pfsql.droptable(self._db, "dirlist", True)
        except Exception:
            print("Error while clearing existing data tables (check recommended)!?")

    def setuptables(self):
        pfsql.createtable(
            self._db, "dirlist", ["id INTEGER PRIMARY KEY", "path type UNIQUE"], True
        )
        self._currentPathID = self.insertPath(self._basePath)

        self._columnNames[0] += " REFERENCES dirlist(id)"
        self._columnNames[-1] += " INTEGER PRIMARY KEY"
        pfsql.createtable(
            self._db, "filelist", self._columnNames, True, "UNIQUE(path, filename)"
        )

        # set all row's file status to -1 (=deleted)
        pfsql.updaterow(self._db, "filelist", "status = ?", None, (-1,))

    def writeStats(self, params):
        """Create statistics table if not existing and append a new row."""
        pfsql.createtable(
            self._db,
            "stats",
            [
                "id INTEGER PRIMARY KEY",
                "timestamp",
                "scanpath",
                "pattern",
                "recurse",
                "filecount",
                "duration",
            ],
            True,
        )
        self._statrowID = pfsql.insertidrow(
            self._db,
            "stats",
            (7 * "?, ").strip(", "),
            (
                None,
                datetime.now(),
                str(params.ScanPath),
                params.Pattern,
                params.Recurse,
                None,
                None,
            ),
        )

    def writeMatch(self, formattedList):
        if not formattedList[0] == self._currentPath:
            self._currentPathID = self.insertPath(
                str(formattedList[0])[self._basePathLen + 1 :]
            )
            self._currentPath = formattedList[0]

        fileID = pfsql.getrowid(
            self._db,
            "filelist",
            f"path={self._currentPathID} AND filename='{formattedList[1]}'",
        )

        formattedList[0] = self._currentPathID

        if fileID is None:
            # append status "1" for new file and None for empty ID
            formattedList.extend([1, None])
            self._dataSets.append([-1, formattedList])
        else:
            # append status "0" for previously existing file and its ID
            formattedList.extend([0, fileID[0]])
            self._dataSets.append([fileID[0], formattedList])

        if len(self._dataSets) == 50:
            self.executeInsertUpdateFiles()

    def flushMatches(self):
        if len(self._dataSets) > 0:
            self.executeInsertUpdateFiles()

    def updateStats(self, countFiles, duration):
        pfsql.updaterow(
            self._db,
            "stats",
            "filecount = ?, duration = ?",
            f"ID={self._statrowID}",
            (countFiles, duration),
        )

    def close(self):
        if self._db is not None:
            pfsql.closedb(self._db)

    def insertPath(self, newPath):
        """If not existing, insert a new path entry into the dirlist table,
        in any way, return its row ID.
        """
        rowID = pfsql.getrowid(self._db, "dirlist", f"path='{newPath}'")

        if rowID is not None:
            return rowID[0]

        return pfsql.insertidrow(self._db, "dirlist", "?, ?", (None, newPath))

    def executeInsertUpdateFiles(self):
        """Insert or update collection with new file datasets into table."""
        try:
            inserts = [i for (rowID, i) in self._dataSets if rowID == -1]
            updates = [i for (rowID, i) in self._dataSets if rowID != -1]

            if len(inserts) > 0:
                self._db[1].executemany(self._insertCmd, inserts)
            if len(updates) > 0:
                self._db[1].executemany(self._updateCmd, updates)
            self._db[0].commit()
        except Exception as e:
            # ignore invalid data
            print(e)
            # pass
        self._dataSets = []
