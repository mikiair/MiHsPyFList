#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2021 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.2"
__date__ = "04/24/2021"

"""List files matching a pattern in a directory and its sub-directories,
and print results to stdout or save as a CSV file
"""

# standard imports
import argparse
import pathlib
import sys

# local imports
import pfllib.PFLParams as PFLParams
import pfllib.PFLArgParse as PFLArgParse
import pfllib.PFLOut as PFLOut

def createPFLOut(params):
    if params.UseStdOut:
        return PFLOut.PFLOutStd()
    else:
        print("Write results to {}".format(params.OutFilePath))
        return PFLOut.PFLOutCSV(params.OutFilePath,
                                ["path","filename"])
    
# define and collect commandline arguments
parser = PFLArgParse.PFLArgParseWUserPattern(description="List files matching a pattern in a directory and its sub-directories\n"
                                             + "and print the results to stdout or save as a CSV file.")
args = parser.parse_args()

try:
    # create parameter object
    params = PFLParams.PFLParams(args.pattern, args.scandir, args.recurse, False, args.outfile)

    # optionally resolve and create output file
    pflOut = createPFLOut(params)
        
    countFiles = 0

    print("Search for files matching '{0}' in directory '{1}'...".format(params.Pattern, params.ScanPath))

    try:
        # search all matching files
        matchingFiles = params.ScanPath.glob(params.Pattern)
        
        # go through the resulting file list and print results to stdout or file
        for match in matchingFiles:
            if not match.is_dir():
                outputColumns = [match.parent,match.name]
                pflOut.writeMatch(outputColumns)

                countFiles += 1
            
    finally:
        # close outfile
        pflOut.close()
            
        if countFiles==0:
            print("Found no matching files.")
        else:
            print("Found {0} matching file(s).".format(countFiles))
except (BaseException) as e:
    print(e.args[0])

