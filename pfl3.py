#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2021 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.1"
__date__ = "04/17/2021"

"""List mp3 files in a directory and its sub-directories,
and print results including mp3 tags to stdout or save as a CSV file
"""

# standard imports
import argparse
import pathlib
import sys
import pfllib

# local imports
import pfllib.PFLParams as PFLParams
import pfllib.PFLArgParse as PFLArgParse

# define and collect commandline arguments
parser = PFLArgParse.PFLArgParse(description="List mp3 files in a directory and its sub-directories\n"
                                 + "and print results including mp3 tags to stdout or save as a CSV file.")
args = parser.parse_args()

class PFLParamsMP3(PFLParams):
    def __init__(self, recurse, scandir, showdots, outfile):
        super().__init__(recurse, "*.mp3", scandir, showdots, outfile)
        