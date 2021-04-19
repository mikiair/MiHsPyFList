#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2021 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.1"
__date__ = "04/18/2021"

"""Class PFLArgParse derives from ArgumentParser and specifies an argument parser with set of default arguments for file listings
"""

# standard imports
from argparse import ArgumentParser
import pathlib

class PFLArgParse(ArgumentParser):
    def __init__(self, description):
        super().__init__(description)
        self.add_argument("--recurse", "-r", dest="recurse", action="store_true", default=False,
                          help="recurse sub-folders")
        self.add_argument("scandir", nargs="?", default=".",
                          help="directory to scan for files [default=current folder]")
        self.add_argument("outfile", nargs="?", type=pathlib.Path, default=None,
                          help="CSV file to write results to [default=stdout]")

class PFLArgParseWPattern(PFLArgParse):
    def __init__(self, description):
        super().__init__(description)
        self.add_argument("pattern", nargs="?", default="*.*",
                          help="only files matching this pattern will be listed")
