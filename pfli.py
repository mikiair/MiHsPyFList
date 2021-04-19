#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2021 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.1"
__date__ = "04/11/2021"

"""List files matching a pattern in a directory and its sub-directories,
and print results including file information to stdout or save as a CSV file
"""

# standard imports
import argparse
import pathlib
import sys
import csv
import os
from datetime import datetime

# local imports
import pfllib.PFLParams as PFLParams
import pfllib.PFLArgParse as PFLArgParse

# define and collect commandline arguments
parser = PFLArgParse.PFLArgParseWPattern(description="List files matching a pattern in a directory and its sub-directories,\n"
                                         + "and print results including file information to stdout or save as a CSV file")
args = parser.parse_args()

# check pattern
if args.pattern.find("*")<0 and args.pattern.find("?")<0:
    print("Pattern without wildcards?!")
    sys.exit(3)
    
# check / resolve directory to scan
if args.scandir==".":
    ScanDir = pathlib.Path.cwd()
else:
    if args.scandir.find("*")>=0 or args.scandir.find("?")>=0:
        print("Invalid wildcards in directory '{0}'!".format(args.scandir))
        sys.exit(3)
    ScanDir = pathlib.Path(args.scandir).resolve()

if not ScanDir.exists():
    print("Directory '{0}' does not exist!".format(ScanDir))
    sys.exit(3)

if not ScanDir.is_dir():
    print("'{0}' is not a directory!".format(ScanDir))
    sys.exit(3)
    
# check output options    
UseStdOut = args.outfile is None

# optionally resolve and create output file 
if not UseStdOut:
    OutFile = open(pathlib.Path(args.outfile).resolve(), "w", newline="")
    print("Write results to {}".format(OutFile.name))
    csvWriter = csv.writer(OutFile, dialect="excel-tab", delimiter=";")
    csvWriter.writerow(["path", "filename", "filesize", "created", "lastwrite"])
    
# get the match pattern
Pattern = "**/" + args.pattern if args.recurse else args.pattern

countFiles = 0
fileDateTimeFormat = "%y-%m-%d %H:%M:%S"

print("Search for files matching '{0}' in directory '{1}'...".format(args.pattern, ScanDir))

try:
    # search all matching files
    matchingFiles = ScanDir.glob(Pattern)
    
    # go through the resulting file list and print results to stdout or file
    for match in matchingFiles:
        try:
            outputColumns = [match.parent,
                             match.name,
                             os.path.getsize(match),
                             datetime.fromtimestamp(os.path.getctime(match)).strftime(fileDateTimeFormat),
                             datetime.fromtimestamp(os.path.getmtime(match)).strftime(fileDateTimeFormat)]
        except:
            outputColumns = [match.parent,
                             match.name, "", "", ""]
            
        if UseStdOut:
            print(outputColumns)
        else:
            csvWriter.writerow(outputColumns)
            OutFile.flush()

        countFiles += 1
        
finally:
    # close outfile
    if not UseStdOut:
        OutFile.close()
        
    if countFiles==0:
        print("Found no matching files.")
    else:
        print("Found {0} matching file(s).".format(countFiles))
