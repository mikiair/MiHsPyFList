#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.2"
__date__ = "07/01/2023"

"""List mp4 files in a directory and its sub-directories,
and print results including mp4 tags to stdout or save as a CSV file
"""

# standard imports
import os
from datetime import datetime

# 3rd party imports
from tinytag import TinyTag

# local imports
import pfllib.pflargparse as pflargparse
import pfllib.pflparams as pflparams
import pfllib.pflrun as pflrun


class PFLParamsMP4(pflparams.PFLParams):
    """Class with fixed search pattern '*.mp4'."""

    def __init__(self, scandir, recurse, outfile, outexistsmode, nodots):
        super().__init__("*.mp4", scandir, recurse, outfile, outexistsmode, nodots)


class PFLRunMP4(pflrun.PFLRun):
    """Derived class for scanning and storage of mp4 file and tag information."""

    def __init__(self, params):
        super().__init__(params)
        self.Columns = [
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

    def getMatchDataList(self, match):
        """Return list with data from the match."""
        try:
            tag = TinyTag.get(match)
            return [
                match.parent,
                match.name,
                datetime.fromtimestamp(os.path.getctime(match)),
                datetime.fromtimestamp(os.path.getmtime(match)),
                round(tag.duration, 3),
                round(tag.bitrate, 0),
                "" if tag.artist is None else tag.artist.strip(),
                tag.title,
                tag.year,
            ]
        except (Exception):
            return [match.parent, match.name, None, None, 0, 0, "", "", "-1"]

    def formatListStrings(self, dataList):
        """Return all elements in the list formatted as strings."""
        return [
            str(dataList[0]),
            str(dataList[1]),
            dataList[2].strftime(self._fileDateTimeFormat)
            if dataList[2] is not None
            else "",
            dataList[3].strftime(self._fileDateTimeFormat)
            if dataList[3] is not None
            else "",
            str(dataList[4]),
            str(dataList[5]),
            dataList[6],
            dataList[7],
            dataList[8],
        ]

    def formatListDatabase(self, dataList):
        """Return all elements in the list converted to types suitable for database."""
        return [
            str(dataList[0]),
            str(dataList[1]),
            dataList[2],
            dataList[3],
            dataList[4],
            dataList[5],
            dataList[6],
            dataList[7],
            int((dataList[8].strip() or -1) if dataList[8] is not None else -1),
        ]


# define and collect commandline arguments
# (kept outside try-catch block to leave exception messages untouched)
parser = pflargparse.PFLArgParseFixedPattern(
    description="List mp4 files in a directory and its sub-directories\n"
    + "and print results including mp4 tags to stdout,\n"
    + "or save as a CSV or database file."
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
        args.dots,
    )

    print("Search for mp4 files in directory '{}'...".format(params.ScanPath))

    run = PFLRunMP4(params)

    run.Run()
except (KeyboardInterrupt):
    print("Cancelled by user!")
except (Exception) as e:
    print("Unhandled error:", e.args[0])
