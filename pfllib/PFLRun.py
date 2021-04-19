#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2021 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.1"
__date__ = "04/17/2021"

"""Class PFLRun defines the base file listing behaviour
"""

# standard imports
import pathlib
import sys

# 3rd party imports

# local imports

class PFLRun:
    def __init__(self, params):
        self._Params = params
    
    def Run(self):
        matchingFiles = ScanDir.glob(params.Pattern)
        
        # go through the resulting file list and print results to stdout or file
        for match in matchingFiles:
            handleMatch(match)
            
    def handleMatch(match):
        pass
    