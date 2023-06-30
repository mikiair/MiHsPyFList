#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.3"
__date__ = "06/30/2023"

"""Class PFLRun defines the basic file listing behaviour.
It takes an PFLParams object and performs a search for files,
handling each match by a virtual method.
"""

# standard imports
import glob
import pathlib
import sys

# local imports
import pfllib.pflout as pflout
import pfllib.pfloutsqlite as pfloutsqlite


class PFLRun:
    """Class PFLRun defines the basic file listing behaviour.
    It takes an PFLParams object and performs a search for files,
    handling each match by a virtual method.
    """

    def __init__(self, params):
        self._params = params
        self._countFiles = 0
        self._columns = []

    def getCountFiles(self, doc="Return the number of matching files found"):
        return self._countFiles

    CountFiles = property(getCountFiles)

    def getColumns(self, doc="Return the columns"):
        return self._columns

    def setColumns(self, columns):
        self._columns = columns

    Columns = property(getColumns, setColumns)

    def Run(self, immediate=True):
        """Run the file search."""
        self.createpflout()

        self._countFiles = 0

        try:
            if immediate:
                # use glob iterator to immediately handle results
                # (does not return folders starting with dot!)
                matchingFiles = glob.iglob(
                    f"{self._params.ScanPath}/{self._params.Pattern}",
                    recursive=True if self._params.Pattern.find("**") >= 0 else False,
                )

                # go through the resulting file list and print results to stdout or file
                for match in matchingFiles:
                    matchPath = pathlib.Path(match)
                    if matchPath.is_file():
                        matchDataList = self.getMatchDataList(matchPath)
                        self._pflout.writeMatch(self._formatMatchList(matchDataList))
                        self._countFiles += 1
            else:
                matchingFiles = self._params.ScanPath.glob(self._params.Pattern)

                # go through the resulting file list and print results to stdout or file
                for match in matchingFiles:
                    if match.is_file():
                        matchDataList = self.getMatchDataList(match)
                        self._pflout.writeMatch(self._formatMatchList(matchDataList))
                        self._countFiles += 1
        finally:
            # close outfile
            self._pflout.close()

            if self._countFiles == 0:
                print("Found no matching files.")
            else:
                print("Found {0} matching file(s).".format(self._countFiles))

    def getMatchDataList(self, match):
        """Return list with data from the match."""
        return None

    def formatListStrings(self, dataList):
        """Return all elements in the list formatted as strings."""
        return [str(e) for e in dataList]

    def formatListDatabase(self, dataList):
        """Return all elements in the list converted to types suitable for database."""
        return dataList

    def createpflout(self):
        """Create the output object for data storage."""
        if self._params.UseStdOut:
            self._pflout = pflout.PFLOutStd()
            self._formatMatchList = self.formatListStrings
        else:
            print("Write results to {}".format(self._params.OutFilePath))
            if self._params.OutFileType == 1:
                self._pflout = pfloutsqlite.PFLOutSqlite(
                    self._params.OutFilePath,
                    self._columns,
                    self._params.ShowDots,
                )
                self._formatMatchList = self.formatListDatabase
            else:
                self._pflout = pflout.PFLOutCSV(
                    self._params.OutFilePath,
                    self._columns,
                    self._params.ShowDots,
                )
                self._formatMatchList = self.formatListStrings

            if self._params.OutExistsMode == "":
                if self._params.OutFilePath.exists():
                    inputres = input("Output file already exists. Overwrite (Y/n)?")
                    if inputres != "" and inputres != "Y" and inputres != "y":
                        sys.exit(0)
                overwrite = "w"
            else:
                overwrite = self._params.OutExistsMode

            self._pflout.openout(overwrite)