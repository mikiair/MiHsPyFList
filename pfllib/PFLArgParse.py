#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2021 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.3"
__date__ = "04/27/2021"

"""Classes in PFLArgParse derive from ArgumentParser and specify different argument parsers with
set of default arguments for file listings (fixed pattern or user defined pattern)
"""

# standard imports
from argparse import ArgumentParser
import pathlib

class PFLArgParseOptionalPattern(ArgumentParser):
    def __init__(self, description, withPattern):
        super().__init__(description)
        self.add_argument("-r", "--recurse", dest="recurse", action="store_true", default=False,
                          help="recurse sub-folders")
        
        if withPattern:
            self.addPatternArgument()
            
        self.add_argument("scandir", nargs="?", default=".",
                          help="directory to scan for files [default=current folder]")
        self.add_argument("outfile", nargs="?", type=pathlib.Path, default=None,
                          help="CSV file to write results to [default=stdout]")

        csvopt_group = self.add_argument_group("CSV file options",
                                               "optional arguments apply when writing to CSV file "
                                               + "(ignored otherwise)")
        
        existmode_group = csvopt_group.add_mutually_exclusive_group()
        
        existmode_group.add_argument("-o", "--overwrite", dest="overwrite",
                                     action="store_const", const="w", default="",
                                     help = "overwrite the outfile if existent")
        existmode_group.add_argument("-a", "--append", dest="append",
                                     action="store_const", const="a", default="",
                                     help = "append to the outfile if existent")

        csvopt_group.add_argument("-n", "--nodots", dest="nodots", action="store_true", default=False,
                                  help="do not display dots for matches")

    def addPatternArgument(self):
        self.add_argument("pattern", nargs="?", default="*.*",
                          help="only files matching this pattern will be listed")
        
class PFLArgParseFixedPattern(PFLArgParseOptionalPattern):
    def __init__(self, description):
        super().__init__(description, False)

class PFLArgParseWUserPattern(PFLArgParseOptionalPattern):
    def __init__(self, description):
        super().__init__(description, True)
