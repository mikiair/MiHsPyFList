#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.2"
__date__ = "06/30/2023"

"""List jpg files in a directory and its sub-directories,
and print results including jpg tags to stdout or save as a CSV file
"""

# standard imports
import os
from datetime import datetime

# local imports
import pfllib.PFLArgParse as PFLArgParse
import pfllib.PFLParams as PFLParams
import pfllib.PFLRun as PFLRun

# 3rd party imports
# from PIL import Image
# from exif import Image as imgEXIF


class PFLParamsJPG(PFLParams.PFLParams):
    """Class with fixed search pattern '*.jpg'."""

    def __init__(self, scandir, recurse, outfile, outexistsmode, nodots):
        super().__init__("*.jpg", scandir, recurse, outfile, outexistsmode, nodots)


class PFLRunJPG(PFLRun.PFLRun):
    """Derived class for scanning and storage of jpg file and image information."""

    def __init__(self, params):
        super().__init__(params)
        self.ColumnHeader = [
            "path",
            "filename",
            "ctime",
            "wtime",
            "size",
            "width",
            "height",
        ]
        self._fileDateTimeFormat = "%Y-%m-%d %H:%M:%S"

    def handleMatch(self, match):
        try:
            return [
                match.parent,
                match.name,
                datetime.fromtimestamp(os.path.getctime(match)).strftime(
                    self._fileDateTimeFormat
                ),
                datetime.fromtimestamp(os.path.getmtime(match)).strftime(
                    self._fileDateTimeFormat
                ),
                os.path.getsize(match),
                "",
                "",
            ]
        except (Exception):
            return [match.parent, match.name, "", "", "", "", ""]


# define and collect commandline arguments
# (kept outside try-catch block to leave exception messages untouched)
parser = PFLArgParse.PFLArgParseFixedPattern(
    description="List jpg files in a directory and its sub-directories\n"
    + "and print results including jpg tags to stdout or save as a CSV file."
)
args = parser.parse_args()

try:
    # create parameter object
    params = PFLParamsJPG(
        args.scandir,
        args.recurse,
        args.outfile,
        args.overwrite + args.append,
        args.nodots,
    )

    print("Search for jpg files in directory '{}'...".format(params.ScanPath))

    run = PFLRunJPG(params)

    run.Run()
except (KeyboardInterrupt):
    print("Cancelled by user!")
except (Exception) as e:
    print("Unhandled error:", e.args[0])
