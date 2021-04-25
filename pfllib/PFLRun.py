#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2021 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.1"
__date__ = "04/25/2021"

"""Class PFLRun defines the basic file listing behaviour.
It takes an PFLParams object and performs a search for files, handling each match by a virtual method
"""

# standard imports
import pathlib
import sys

# local imports
import pfllib.PFLOut as PFLOut

class PFLRun:
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
    
    def Run(self):
        self.createPFLOut()
        
        self._countFiles = 0

        try:
            matchingFiles = self._Params.ScanPath.glob(self._Params.Pattern)
            
            # go through the resulting file list and print results to stdout or file
            for match in matchingFiles:
                if not match.is_dir():
                    outputColumns = self.handleMatch(match)
                    self._pflOut.writeMatch(outputColumns)
                    self._countFiles += 1
        finally:
            # close outfile
            self._pflOut.close()
                
            if self._countFiles==0:
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
            self._pflOut = PFLOut.PFLOutCSV(self._Params.OutFilePath, self._Params.OutExistsMode,
                                            self._columnHeader, self._Params.ShowDots)
            
            if self._Params.OutExistsMode=="":
                if self._Params.OutFilePath.exists():
                    inputres = input("Output file already exists. Overwrite (Y/n)?")
                    if inputres != "" and inputres != "Y" and inputres != "y":
                        sys.exit( 0 );
                overwrite = "w"
            else:
                overwrite = self._Params.OutExistsMode
            
            self._pflOut.openout(overwrite)