#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2021 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.1"
__date__ = "04/11/2021"

"""List files matching a pattern in a directory and its sub-directories,
and print results to stdout or save as a CSV file
"""

# standard imports
import argparse
import pathlib
import sys
import csv

# local imports
import pfllib.PFLParams as PFLParams
import pfllib.PFLArgParse as PFLArgParse

# define and collect commandline arguments
parser = PFLArgParse.PFLArgParseWPattern(description="List files matching a pattern in a directory and its sub-directories\n"
                                         +"and print the results to stdout or save as a CSV file.")
args = parser.parse_args()

# check / resolve directory to scan
if args.scandir==".":
    ScanDir = pathlib.Path.cwd()
else:
    if args.scandir.find("*")>=0 or args.scandir.find("?")>=0:
        print("Invalid wildcards in directory '{0}'!".format(args.scandir))
        sys.exit(3)
    ScanDir = pathlib.Path(args.scandir).resolve()

try:
    # create parameter object
    params = PFLParams.PFLParams(args.pattern, ScanDir, args.recurse, False, args.outfile)

    # optionally resolve and create output file 
    if not params.UseStdOut:
        OutFile = open(pathlib.Path(args.outfile).resolve(), "w", newline="")
        print("Write results to {}".format(OutFile.name))
        csvWriter = csv.writer(OutFile, dialect="excel-tab", delimiter=";")
        csvWriter.writerow(["path", "filename"])

    countFiles = 0

    print("Search for files matching '{0}' in directory '{1}'...".format(params.Pattern, params.ScanDir))

    try:
        # search all matching files
        matchingFiles = ScanDir.glob(params.Pattern)
        
        # go through the resulting file list and print results to stdout or file
        for match in matchingFiles:
            outputColumns = [match.parent,match.name]
            if params.UseStdOut:
                print(outputColumns)
            else:
                csvWriter.writerow(outputColumns)
                OutFile.flush()

            countFiles += 1
            
    finally:
        # close outfile
        if not params.UseStdOut:
            OutFile.close()
            
        if countFiles==0:
            print("Found no matching files.")
        else:
            print("Found {0} matching file(s).".format(countFiles))
except (BaseException) as e:
    print(e.args[0])

