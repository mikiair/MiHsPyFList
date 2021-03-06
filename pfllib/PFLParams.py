#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2021 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.2"
__date__ = "04/25/2021"

"""Class PFLParams defines a set of parameters used for searching files:
a match pattern, a directory to scan, option to recurse into sub-folders, and a file for result output,
and additional attribute for stdout usage
"""

# standard imports
import pathlib

# 3rd party imports

# local imports

class PFLParams:
    def __init__(self, pattern, scandir, recurse, outfile, outexistsmode, nodots):
        self._Pattern = pattern
        self._ScanDir = scandir
        self._Recurse = recurse
        self._OutFile = outfile
        self._UseStdOut = outfile is None
        self._OutExistsMode = outexistsmode
        self._ShowDots = outfile is not None and not nodots
        self.IsValid()

    def getPattern(self, doc="The glob-usable match pattern for the files to search for"):
        return "**/" + self._Pattern if self._Recurse else self._Pattern
    Pattern = property(getPattern)
    
    def getScanPath(self, doc="The path to the folder to scan for files"):
        return self._ScanPath
    ScanPath = property(getScanPath)
    
    def getRecurse(self, doc="If true, scan will recurse into sub-folders"):
        return self._Recurse
    Recurse = property(getRecurse)
    
    def getOutFilePath(self, doc="Determines the filename of the output file"):
        return self._OutFilePath
    OutFilePath = property(getOutFilePath)
    
    def getUseStdOut(self, doc="If true, use stdout to print results"):
        return self._UseStdOut
    UseStdOut = property(getUseStdOut)
    
    def getOutExistsMode(self, doc="Defines the way an existing outfile will be handled"):
        return self._OutExistsMode
    OutExistsMode = property(getOutExistsMode)
    
    def getShowDots(self, doc="If true, stdout will display a dot for each matching file (when writing to file)"):
        return self._ShowDots
    ShowDots = property(getShowDots)

    def IsValid(self):
        if self._Pattern.find("*")<0 and self._Pattern.find("?")<0:
            raise ValueError("Pattern without wildcards?!")
        
        if self._ScanDir.find("*")>=0 or self._ScanDir.find("?")>=0:
            raise ValueError("Invalid wildcards in directory '{0}'!".format(self._ScanDir))
        
        self.resolveScanPath(self._ScanDir)
        
        if not self._ScanPath.exists():
            raise FileNotFoundError("Directory '{0}' does not exist!".format(self._ScanPath))
        if not self._ScanPath.is_dir():
            raise NotADirectoryError("'{0}' is not a directory!".format(self._ScanPath))
        
        self.resolveOutFilePath(self._OutFile)
        
        return True
    
    def resolveScanPath(self, scandir):
        self._ScanPath = pathlib.Path.cwd() if scandir  == "." else pathlib.Path(scandir).resolve()

    def resolveOutFilePath(self, outfile):
        self._OutFilePath = pathlib.Path(outfile).resolve() if not outfile is None else None
        