#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.1.1"
__date__ = "07/15/2023"

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


class PFLArgParseWUserPatternAndLimit(pflargparse.PFLArgParseWUserPattern):
    """Argument parser class adding an option to limit scanned file size
    used for hashing.
    """

    def __init__(self, description):
        super().__init__(description)
        self.add_argument(
            "-l",
            "--limit",
            dest="limit",
            action="store_true",
            default=False,
            help="limit the scanned file size for hash value calculation to 100MB",
        )


# def check_positive(value):
#     ivalue = int(value)
#     if ivalue < 0:
#         raise argparse.ArgumentTypeError("Limit must be a positive integer value or zero!")
#     return ivalue


class PFLParamsWithLimit(pflparams.PFLParams):
    """Parameter class with additional file hash size limit."""

    def __init__(self, args):
        super().__init__(args)
        self._IsLimited = args.limit

    def getIsLimited(
        self, doc="Return true if the file size for hashing will be limited"
    ):
        return self._IsLimited

    IsLimited = property(getIsLimited)


class PFLRunFileInfoWithSHA256(pflrun.PFLRun):
    """Derived class for scanning and storage of file information including SHA256 hash."""

    BIGFILESIZELIMIT = 100 * 1024 * 1024

    def __init__(self, params):
        super().__init__(params)
        self.Columns = ["path", "filename", "size", "ctime", "wtime", "hash"]
        self._fileDateTimeFormat = "%Y-%m-%d %H:%M:%S"

    def getMatchDataList(self, match):
        """Return list with data from the match."""
        try:
            stat = os.stat(match)
            if stat.st_size > 0:
                if params.IsLimited and stat.st_size > self.BIGFILESIZELIMIT:
                    hashbytes = self.getHashBytesLimited(match)
                else:
                    hashbytes = self.getHashBytes(match)
            else:
                hashbytes = None

            return [
                match.parent,
                match.name,
                stat.st_size,
                datetime.fromtimestamp(stat.st_ctime),
                datetime.fromtimestamp(stat.st_mtime),
                hashbytes,
            ]
        except Exception:
            return [match.parent, match.name, -1, None, None, None]

    def getHashBytesLimited(self, filename):
        """Return the SHA256 hash of the file scanning only the first 100MB."""
        hashsha = hashlib.sha256()  # create a new object for each file!
        with open(filename, "rb") as f:
            bytesRead = 0
            for block in iter(lambda: f.read(8192), b""):
                hashsha.update(block)
                bytesRead += len(block)
                if bytesRead >= self.BIGFILESIZELIMIT:
                    break
        return hashsha.digest()

    def getHashBytes(self, filename):
        """Return the SHA256 hash of the file."""
        hashsha = hashlib.sha256()  # create a new object for each file!
        with open(filename, "rb") as f:
            for block in iter(lambda: f.read(8192), b""):
                hashsha.update(block)
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
            dataList[5].hex() if dataList[5] is not None else "",
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
parser = PFLArgParseWUserPatternAndLimit(
    description="List files matching a pattern in a directory and its sub-directories,\n"
    + "and print results including file information with SHA256 to stdout,\n"
    + "or save as a CSV or database file."
)
args = parser.parse_args()

try:
    # create parameter object
    params = PFLParamsWithLimit(args)

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
