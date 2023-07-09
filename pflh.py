#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.1.0"
__date__ = "07/09/2023"

"""List files matching a pattern in a directory and its sub-directories,
and print results including file information (with SHA256 hash)
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


class PFLRunFileInfoWithSHA256(pflrun.PFLRun):
    """Derived class for scanning and storage of file information including SHA256 hash."""

    def __init__(self, params):
        super().__init__(params)
        self.Columns = ["path", "filename", "size", "ctime", "wtime", "hash"]
        self._fileDateTimeFormat = "%Y-%m-%d %H:%M:%S"

    def getMatchDataList(self, match):
        """Return list with data from the match."""
        try:
            hashbytes = self.getHashBytes(match)
            return [
                match.parent,
                match.name,
                os.path.getsize(match),
                datetime.fromtimestamp(os.path.getctime(match)),
                datetime.fromtimestamp(os.path.getmtime(match)),
                hashbytes,
            ]
        except Exception:
            return [match.parent, match.name, -1, None, None]

    def getHashBytes(self, filename, blocksize=65536):
        """Return the SHA256 hash of the file."""
        hashsha = hashlib.sha256()  # create a new object for each file!
        with open(filename, "rb") as f:
            for block in iter(lambda: f.read(blocksize), b""):
                hashsha.update(block)
            # requires Python >v3.7: digest = hashlib.file_digest(f, "sha256")
        return hashsha.digest()

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
    + "and print results including file information with SHA256 to stdout,\n"
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

    run = PFLRunFileInfoWithSHA256(params)

    run.Run(False)
except (ValueError) as e:
    print(f"Invalid parameter: {e.args[0]}")
except (FileNotFoundError) as e:
    print(f"Directory not found: {e.args[0]}")
except (NotADirectoryError) as e:
    print(f"Error: {e.args[0]}")
except (KeyboardInterrupt):
    print("Cancelled by user!")
except (Exception) as e:
    print("Unhandled error:", e.args[0])
