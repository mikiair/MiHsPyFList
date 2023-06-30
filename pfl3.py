#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.3"
__date__ = "06/30/2023"

"""List mp3 files in a directory and its sub-directories,
and print results including mp3 tags to stdout or save as a CSV file.
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


class PFLParamsMP3(PFLParams.PFLParams):
    """Class with fixed search pattern '*.mp3'"""

    def __init__(self, scandir, recurse, outfile, outexistsmode, nodots):
        super().__init__("*.mp3", scandir, recurse, outfile, outexistsmode, nodots)


class PFLRunMP3(PFLRun.PFLRun):
    """Derived class for scanning and storage of mp3 file and tag information."""

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
            "album",
            "track",
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
                "" if tag.album is None else tag.album.strip(),
                tag.track,
                tag.title,
                tag.year,
            ]
        except (Exception):
            return [match.parent, match.name, "", "", "", "", "", "", "", "", ""]


# define and collect commandline arguments
# (kept outside try-catch block to leave exception messages untouched)
parser = PFLArgParse.PFLArgParseFixedPattern(
    description="List mp3 files in a directory and its sub-directories\n"
    + "and print results including mp3 tags to stdout or save as a CSV file."
)
args = parser.parse_args()

try:
    # create parameter object
    params = PFLParamsMP3(
        args.scandir,
        args.recurse,
        args.outfile,
        args.overwrite + args.append,
        args.nodots,
    )

    print("Search for mp3 files in directory '{}'...".format(params.ScanPath))

    run = PFLRunMP3(params)

    run.Run()
except (KeyboardInterrupt):
    print("Cancelled by user!")
except (Exception) as e:
    print("Unhandled error:", e.args[0])
