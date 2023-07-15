#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.2.0"
__date__ = "07/15/2023"

"""Classes in pflout handle the output to stdout or to a CSV writer file
"""

# standard imports
import csv


class PFLOut:
    """Abstract base class for result output."""

    def __init__(self):
        pass

    def openout(self, mode):
        pass

    def writeMatch(self, formattedList):
        pass

    def flushMatches(self):
        pass

    def close(self):
        pass


class PFLOutStd(PFLOut):
    """Class for result output to stdout."""

    def __init__(self):
        self._currentFolder = ""

    def writeMatch(self, formattedList):
        """Print file data to stdout. If file is from next folder first print the
        folder name in a separate line.
        """
        if not formattedList[0] == self._currentFolder:
            self._currentFolder = formattedList[0]
            print(self._currentFolder + ":")
        if len(formattedList) > 2:
            joinedOut = "\t" + formattedList[1] + " - " + "/".join(formattedList[2:])
            if len(joinedOut) > 100:
                joinedOut = joinedOut[:100] + "..."
            print(joinedOut)
        else:
            print("\t" + formattedList[1])


class PFLOutFile(PFLOut):
    """Class for result output to a file."""

    def __init__(self, filePath, columnNames):
        self._filePath = filePath
        self._columnNames = columnNames


class PFLOutCSV(PFLOutFile):
    """Class for result output to CSV file."""

    def __init__(self, filePath, columnNames):
        super().__init__(filePath, columnNames)
        self._outFile = None

    def openout(self, mode):
        self._outFile = open(self._filePath, mode, newline="")
        self._csvWriter = csv.writer(self._outFile, dialect="excel-tab", delimiter=";")
        self._csvWriter.writerow(self._columnNames)

    def writeMatch(self, formattedList):
        """Write result data as a new line into CSV file."""
        try:
            self._csvWriter.writerow(formattedList)
        except (Exception):
            # handle invalid chars or invalidly encoded chars
            self._csvWriter.writerow(["Error in output encoding!"])
        self._outFile.flush()

    def close(self):
        if self._outFile is not None:
            self._outFile.close()
