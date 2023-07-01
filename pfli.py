#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.4"
__date__ = "07/01/2022"

"""List files matching a pattern in a directory and its sub-directories,
and print results including file information to stdout or save as a CSV file
"""

# standard imports
import os
from datetime import datetime

# local imports
import pfllib.pflargparse as pflargparse
import pfllib.pflparams as pflparams
import pfllib.pflrun as pflrun


class PFLRunFileInfo(pflrun.PFLRun):
    """Derived class for scanning and storage of file information."""

    def __init__(self, params):
        super().__init__(params)
        self.Columns = ["path", "filename", "size", "ctime", "wtime"]
        self._fileDateTimeFormat = "%Y-%m-%d %H:%M:%S"

    def getMatchDataList(self, match):
        """Return list with data from the match."""
        try:
            return [
                match.parent,
                match.name,
                os.path.getsize(match),
                datetime.fromtimestamp(os.path.getctime(match)),
                datetime.fromtimestamp(os.path.getmtime(match)),
            ]
        except Exception:
            return [match.parent, match.name, -1, None, None]

    def formatListStrings(self, dataList):
        """Return all elements in the list formatted as strings."""
        return [
            str(dataList[0]),
            str(dataList[1]),
            str(dataList[2]),
            dataList[3].strftime(self._fileDateTimeFormat)
            if dataList[3] is not None
            else "",
            dataList[4].strftime(self._fileDateTimeFormat)
            if dataList[4] is not None
            else "",
        ]

    def formatListDatabase(self, dataList):
        """Return all elements in the list converted to types suitable for database."""
        return [
            str(dataList[0]),
            str(dataList[1]),
            dataList[2],
            dataList[3],
            dataList[4],
        ]


# define and collect commandline arguments
# (kept outside try-catch block to leave exception messages untouched)
parser = pflargparse.PFLArgParseWUserPattern(
    description="List files matching a pattern in a directory and its sub-directories,\n"
    + "and print results including file information to stdout,\n"
    + "or save as a CSV or database file."
)
args = parser.parse_args()

try:
    # create parameter object
    params = pflparams.PFLParams(
        args.pattern,
        args.scandir,
        args.recurse,
        args.outfile,
        args.overwrite + args.append,
        args.nodots,
        args.dots,
    )

    print(
        "Search for files matching '{0}' in directory '{1}'...".format(
            args.pattern, params.ScanPath
        )
    )

    run = PFLRunFileInfo(params)

    run.Run(False)
except (KeyboardInterrupt):
    print("Cancelled by user!")
except (Exception) as e:
    print("Unhandled error:", e.args[0])
