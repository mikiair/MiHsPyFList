#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.2"
__date__ = "06/30/2023"

"""Classes in PFLOut handle the output to stdout or to a CSV writer file
"""

# standard imports
import csv


class PFLOut:
    def __init__(self):
        pass

    def openout(self, mode):
        pass

    def writeMatch(self, formattedList):
        pass

    def close(self):
        pass


class PFLOutStd(PFLOut):
    def __init__(self):
        pass

    def writeMatch(self, formattedList):
        print(formattedList)


class PFLOutCSV(PFLOut):
    def __init__(self, filePath, columnNames, showdots):
        self._filePath = filePath
        self._columnNames = columnNames
        self._showDots = showdots

    def openout(self, mode):
        self._outFile = open(self._filePath, mode, newline="")
        self._csvWriter = csv.writer(self._outFile, dialect="excel-tab", delimiter=";")
        self._csvWriter.writerow(self._columnNames)

    def writeMatch(self, formattedList):
        try:
            self._csvWriter.writerow(formattedList)
        except (Exception):
            # handle invalid chars or invalidly encoded chars
            self._csvWriter.writerow(["Error in output encoding!"])
        self._outFile.flush()
        if self._showDots:
            print(".", end="")

    def close(self):
        self._outFile.close()
        if self._showDots:
            print("")
