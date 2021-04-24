#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2021 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.1"
__date__ = "04/24/2021"

"""List mp3 files in a directory and its sub-directories,
and print results including mp3 tags to stdout or save as a CSV file
"""

# standard imports
import argparse
import pathlib
import sys
import pfllib

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
                                ["path","filename","length","interpret","album","titleno","title","year"])

class PFLParamsMP3(PFLParams):
    def __init__(self, scandir, recurse, showdots, outfile):
        super().__init__("*.mp3", scandir, recurse, showdots, outfile)
        
# define and collect commandline arguments
parser = PFLArgParse.PFLArgParse(description="List mp3 files in a directory and its sub-directories\n"
                                 + "and print results including mp3 tags to stdout or save as a CSV file.")
args = parser.parse_args()

try:
    # create parameter object
    params = PFLParams.PFLParamsMP3(args.scandir, args.recurse, False, args.outfile)

    # optionally resolve and create output file 
    pflOut = createPFLOut(params)
        
    countFiles = 0
    fileDateTimeFormat = "%y-%m-%d %H:%M:%S"

    print("Search for mp3 files in directory '{}'...".format(params.ScanPath))

    try:
        # search all matching files
        matchingFiles = params.ScanPath.glob(params.Pattern)
        
        # go through the resulting file list and print results to stdout or file
        for match in matchingFiles:
            if not match.is_dir():
                try:
                    outputColumns = [match.parent,
                                     match.name]
                except:
                    outputColumns = [match.parent,
                                     match.name]
                
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
