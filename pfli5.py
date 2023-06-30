#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.1"
__date__ = "06/30/2022"

"""List files matching a pattern in a directory and its sub-directories,
and print results including file information (with MD5 hash)
to stdout or save as a CSV file.
"""

# standard imports
import hashlib
import os
from datetime import datetime

# local imports
import pfllib.pflargparse as pflargparse
import pfllib.pflparams as pflparams
import pfllib.pflrun as pflrun


class PFLRunFileInfoWithMD5(pflrun.PFLRun):
    """Derived class for scanning and storage of file information including MD5 hash."""

    def __init__(self, params):
        super().__init__(params)
        self.Columns = ["path", "filename", "size", "ctime", "wtime", "md5"]
        self._fileDateTimeFormat = "%Y-%m-%d %H:%M:%S"

    def getMatchDataList(self, match):
        """Return list with data from the match."""
        try:
            md5bytes = self.md5(match)
            return [
                match.parent,
                match.name,
                os.path.getsize(match),
                datetime.fromtimestamp(os.path.getctime(match)),
                datetime.fromtimestamp(os.path.getmtime(match)),
                md5bytes,
            ]
        except Exception:
            return [match.parent, match.name, -1, None, None]

    def md5(self, filename, blocksize=65536):
        """Return the MD5 hash of the file."""
        hashmd5 = hashlib.md5()                      # create a new object for each file!
        with open(filename, "rb") as f:
            for block in iter(lambda: f.read(blocksize), b""):
                hashmd5.update(block)
            # requires Python >v3.7: digest = hashlib.file_digest(f, "md5")
        return hashmd5.digest()

    def formatListStrings(self, dataList):
        """Return all elements in the list formatted as strings."""
        return [
            str(dataList[0]),
            str(dataList[1]),
            str(dataList[2]),
            dataList[3].strftime(self._fileDateTimeFormat),
            dataList[4].strftime(self._fileDateTimeFormat),
            dataList[5].hex(),
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
        ]


# define and collect commandline arguments
# (kept outside try-catch block to leave exception messages untouched)
parser = pflargparse.PFLArgParseWUserPattern(
    description="List files matching a pattern in a directory and its sub-directories,\n"
    + "and print results including file information with MD5 to stdout,\n"
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
    )

    print(
        "Search for files matching '{0}' in directory '{1}'...".format(
            args.pattern, params.ScanPath
        )
    )

    run = PFLRunFileInfoWithMD5(params)

    run.Run(False)
except (KeyboardInterrupt):
    print("Cancelled by user!")
except (Exception) as e:
    print("Unhandled error:", e.args[0])
