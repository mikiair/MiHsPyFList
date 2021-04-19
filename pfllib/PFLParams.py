#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2021 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.1"
__date__ = "04/18/2021"

"""Class PFLParams defines a set of parameters used for searching files:
a match pattern, a directory to scan, option to recurse into sub-folders, and a file for result output,
and additional attribute for stdout usage
"""

# standard imports
import argparse
import pathlib
import sys

# 3rd party imports

# local imports

class PFLParams:
    def __init__(self, pattern, scandir, recurse, showdots, outfile):
        self._Pattern = pattern
        self._ScanDir = scandir
        self._Recurse = recurse
        self._OutFile = outfile
        self._UseStdOut = outfile is None
        self._ShowDots = showdots
        if not self.IsValid():
            raise ArgumentException("Paramters not valid")

    def getPattern(self, doc="The match pattern for the files to search for"):
        return "**/" + self._Pattern if self._Recurse else self._Pattern
    Pattern = property(getPattern)
    
    def getScanDir(self, doc="The directory to scan for files"):
        return self._ScanDir
    ScanDir = property(getScanDir)
    
    def getRecurse(self, doc="If true, scan will recurse into sub-folders"):
        return self._Recurse
    Recurse = property(getRecurse)
    
    def getOutFile(self, doc="Determines the filename of the output file"):
        return self._OutFile
    OutFile = property(getOutFile)
    
    def getUseStdOut(self, doc="If true, use stdout to print results"):
        return self._UseStdOut
    UseStdOut = property(getUseStdOut)
    
    def getShowDots(self, doc="If true, stdout will display a dot for each matching file"):
        return self._ShowDots
    ShowDots = property(getShowDots)
    
    def IsValid(self):
        if self._Pattern.find("*")<0 and self._Pattern.find("?")<0:
            raise ValueError("Pattern without wildcards?!")
        if not self._ScanDir.exists():
            raise FileNotFoundError("Directory '{0}' does not exist!".format(self._ScanDir))
        if not self._ScanDir.is_dir():
            raise NotADirectoryError("'{0}' is not a directory!".format(self._ScanDir))
        return True