#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2021 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.1"
__date__ = "04/24/2021"

"""Classes in PFLOut handle the output to stdout or to a CSV writer file
"""

# standard imports
import csv

class PFLOut:
    def __init__(self):
        pass
    
    def writeMatch(self, outputColumns):
        pass

    def close(self):
        pass
    
class PFLOutStd(PFLOut):
    def __init__(self):
        pass
    
    def writeMatch(self, outputColumns):
        print(outputColumns)
        
class PFLOutCSV(PFLOut):
    def __init__(self, filePath, colheader):
        self._outFile = open(filePath, "w", newline="")
        self._csvWriter = csv.writer(self._outFile, dialect="excel-tab", delimiter=";")
        self._csvWriter.writerow(colheader)
        
    def writeMatch(self, outputColumns):
        self._csvWriter.writerow(outputColumns)
        self._outFile.flush()

    def close(self):
        self._outFile.close()