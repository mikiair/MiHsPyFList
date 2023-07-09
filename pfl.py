#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2023 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.1.0"
__date__ = "07/09/2023"

"""List files matching a pattern in a directory and its sub-directories,
and print results to stdout, save as a CSV file or write to a sqlite3 database.
"""

# local imports
import pfllib.pflargparse as pflargparse
import pfllib.pflparams as pflparams
import pfllib.pflrun as pflrun


class PFLRunFileName(pflrun.PFLRun):
    """Derived class for scanning and storage of file path and name."""

    def __init__(self, params):
        super().__init__(params)
        self.Columns = ["path", "filename"]

    def getMatchDataList(self, match):
        """Return list with data from the match."""
        return [match.parent, match.name]


# define and collect commandline arguments
# (kept outside try-catch block to leave exception messages untouched)
parser = pflargparse.PFLArgParseWUserPattern(
    description="List files matching a pattern in a directory and its sub-directories\n"
    + "and print the results to stdout, or save as a CSV or database file."
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

    run = PFLRunFileName(params)

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
