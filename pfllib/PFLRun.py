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
import pfllib.PFLOut as PFLOut


class PFLRun:
    """Class PFLRun defines the basic file listing behaviour.
    It takes an PFLParams object and performs a search for files,
    handling each match by a virtual method.
    """

    def __init__(self, params):
        self._Params = params
        self._countFiles = 0
        self._columnHeader = []

    def getCountFiles(self, doc="Return the number of matching files found"):
        return self._countFiles

    CountFiles = property(getCountFiles)

    def getColumnHeader(self, doc="Return the column header"):
        return self._columnHeader

    def setColumnHeader(self, columnHeader):
        self._columnHeader = columnHeader

    ColumnHeader = property(getColumnHeader, setColumnHeader)

    def Run(self, immediate=True):
        self.createPFLOut()

        self._countFiles = 0

        try:
            if immediate:
                # use glob iterator to immediately handle results
                # (does not return folders starting with dot!)
                matchingFiles = glob.iglob(
                    f"{self._Params.ScanPath}/{self._Params.Pattern}",
                    recursive=True if self._Params.Pattern.find("**") >= 0 else False,
                )

                # go through the resulting file list and print results to stdout or file
                for match in matchingFiles:
                    matchPath = pathlib.Path(match)
                    if matchPath.is_file():
                        outputColumns = self.handleMatch(matchPath)
                        self._pflOut.writeMatch(outputColumns)
                        self._countFiles += 1
            else:
                matchingFiles = self._Params.ScanPath.glob(self._Params.Pattern)

                # go through the resulting file list and print results to stdout or file
                for match in matchingFiles:
                    if match.is_file():
                        outputColumns = self.handleMatch(match)
                        self._pflOut.writeMatch(outputColumns)
                        self._countFiles += 1
        finally:
            # close outfile
            self._pflOut.close()

            if self._countFiles == 0:
                print("Found no matching files.")
            else:
                print("Found {0} matching file(s).".format(self._countFiles))

    def handleMatch(self, match):
        return None

    def createPFLOut(self):
        if self._Params.UseStdOut:
            self._pflOut = PFLOut.PFLOutStd()
        else:
            print("Write results to {}".format(self._Params.OutFilePath))
            self._pflOut = PFLOut.PFLOutCSV(
                self._Params.OutFilePath,
                self._Params.OutExistsMode,
                self._columnHeader,
                self._Params.ShowDots,
            )

            if self._Params.OutExistsMode == "":
                if self._Params.OutFilePath.exists():
                    inputres = input("Output file already exists. Overwrite (Y/n)?")
                    if inputres != "" and inputres != "Y" and inputres != "y":
                        sys.exit(0)
                overwrite = "w"
            else:
                overwrite = self._Params.OutExistsMode

            self._pflOut.openout(overwrite)
