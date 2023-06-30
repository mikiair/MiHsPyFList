#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.5"
__date__ = "06/30/2023"

"""List files matching a pattern in a directory and its sub-directories,
and print results to stdout, save as a CSV file or write to a sqlite3 database.
"""

# local imports
import pfllib.PFLArgParse as PFLArgParse
import pfllib.PFLParams as PFLParams
import pfllib.PFLRun as PFLRun


class PFLRunFileName(PFLRun.PFLRun):
    """Derived class for scanning and storage of file path and name."""

    def __init__(self, params):
        super().__init__(params)
        self.ColumnHeader = ["path", "filename"]

    def handleMatch(self, match):
        return [match.parent, match.name]


# define and collect commandline arguments
# (kept outside try-catch block to leave exception messages untouched)
parser = PFLArgParse.PFLArgParseWUserPattern(
    description="List files matching a pattern in a directory and its sub-directories\n"
    + "and print the results to stdout or save as a CSV file."
)
args = parser.parse_args()

try:
    # create parameter object
    params = PFLParams.PFLParams(
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

    run = PFLRunFileName(params)

    run.Run(False)
except (KeyboardInterrupt):
    print("Cancelled by user!")
except (Exception) as e:
    print("Unhandled error:", e.args[0])
