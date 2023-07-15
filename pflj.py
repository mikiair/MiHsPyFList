#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.2.0"
__date__ = "07/15/2023"

"""List jpg files in a directory and its sub-directories,
and print results including jpg tags to stdout or save as a CSV file
"""

# standard imports
import os
from datetime import datetime

# 3rd party imports
from PIL import Image

# local imports
import pfllib.pflargparse as pflargparse
import pfllib.pflparams as pflparams
import pfllib.pflrun as pflrun

# from exif import Image as imgEXIF


class PFLParamsJPG(pflparams.PFLParams):
    """Class with fixed search pattern '*.jpg'."""

    def __init__(self, args):
        super().__init__(args, fixpattern="*.jpg")


class PFLRunJPG(pflrun.PFLRun):
    """Derived class for scanning and storage of jpg file and image information."""

    def __init__(self, params):
        super().__init__(params)
        self.Columns = [
            "path",
            "filename",
            "ctime",
            "wtime",
            "size",
            "width",
            "height",
        ]
        self._fileDateTimeFormat = "%Y-%m-%d %H:%M:%S"

    def getMatchDataList(self, match):
        """Return list with data from the match."""
        try:
            im = Image.open(match)
            width, height = im.size
            return [
                match.parent,
                match.name,
                datetime.fromtimestamp(os.path.getctime(match)),
                datetime.fromtimestamp(os.path.getmtime(match)),
                os.path.getsize(match),
                width,
                height,
            ]
        except (Exception):
            return [match.parent, match.name, None, None, -1, -1, -1]

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
            str(dataList[6]),
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
        ]


# define and collect commandline arguments
# (kept outside try-catch block to leave exception messages untouched)
parser = pflargparse.PFLArgParseFixedPattern(
    description="List jpg files in a directory and its sub-directories\n"
    + "and print results including jpg tags to stdout,\n"
    + "or save as a CSV or database file."
)
args = parser.parse_args()

try:
    # create parameter object
    params = PFLParamsJPG(args)

    print("Search for jpg files in directory '{}'...".format(params.ScanPath))

    run = PFLRunJPG(params)

    run.Run()
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
