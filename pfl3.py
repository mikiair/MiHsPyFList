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

# 3rd party imports

# local imports

# define commandline arguments
parser = argparse.ArgumentParser(description="List mp3 files in a directory and its sub-directories\n"
                                 +"and print results including mp3 tags to stdout or save as a CSV file.")
parser.add_argument("--recurse", "-r", dest="recurse", action="store_true", default=False,
                    help="recurse sub-folders")
parser.add_argument("scandir", nargs="?", default=".",
                    help="directory to scan for files")
parser.add_argument("outfile", nargs="?", type=pathlib.Path, default=None,
                    help="CSV file to write results to [default=stdout]")

# collect commandline arguments
args = parser.parse_args()

class PFLParamsMP3(PFLParams):
    def __init__(self, recurse, scandir, outfile):
        super().__init__(recurse, "*.mp3", scandir, outfile)
        