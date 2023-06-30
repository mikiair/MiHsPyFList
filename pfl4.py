#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.2"
__date__ = "06/30/2023"

"""List mp4 files in a directory and its sub-directories,
and print results including mp4 tags to stdout or save as a CSV file
"""

# standard imports
import os
from datetime import datetime

# 3rd party imports
from tinytag import TinyTag

# local imports
import pfllib.PFLArgParse as PFLArgParse
import pfllib.PFLParams as PFLParams
import pfllib.PFLRun as PFLRun


class PFLParamsMP4(PFLParams.PFLParams):
    """Class with fixed search pattern '*.mp4'."""

    def __init__(self, scandir, recurse, outfile, outexistsmode, nodots):
        super().__init__("*.mp4", scandir, recurse, outfile, outexistsmode, nodots)


class PFLRunMP4(PFLRun.PFLRun):
    """Derived class for scanning and storage of mp4 file and tag information."""

    def __init__(self, params):
        super().__init__(params)
        self.ColumnHeader = [
            "path",
            "filename",
            "ctime",
            "wtime",
            "length",
            "bitrate",
            "artist",
            "title",
            "year",
        ]
        self._fileDateTimeFormat = "%Y-%m-%d %H:%M:%S"

    def handleMatch(self, match):
        try:
            tag = TinyTag.get(match)
            return [
                match.parent,
                match.name,
                datetime.fromtimestamp(os.path.getctime(match)).strftime(
                    self._fileDateTimeFormat
                ),
                datetime.fromtimestamp(os.path.getmtime(match)).strftime(
                    self._fileDateTimeFormat
                ),
                round(tag.duration, 3),
                round(tag.bitrate, 0),
                tag.artist,
                tag.title,
                tag.year,
            ]
        except (Exception):
            return [match.parent, match.name, "", "", "", "", "", "", ""]


# define and collect commandline arguments
# (kept outside try-catch block to leave exception messages untouched)
parser = PFLArgParse.PFLArgParseFixedPattern(
    description="List mp4 files in a directory and its sub-directories\n"
    + "and print results including mp4 tags to stdout or save as a CSV file."
)
args = parser.parse_args()

try:
    # create parameter object
    params = PFLParamsMP4(
        args.scandir,
        args.recurse,
        args.outfile,
        args.overwrite + args.append,
        args.nodots,
    )

    print("Search for mp4 files in directory '{}'...".format(params.ScanPath))

    run = PFLRunMP4(params)

    run.Run()
except (KeyboardInterrupt):
    print("Cancelled by user!")
except (Exception) as e:
    print("Unhandled error:", e.args[0])
