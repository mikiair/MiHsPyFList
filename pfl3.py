#!/usr/bin/env python

__author__ = "Michael Heise"
__copyright__ = "Copyright (C) 2021 by Michael Heise"
__license__ = "LGPL"
__version__ = "0.0.1"
__date__ = "04/25/2021"

"""List mp3 files in a directory and its sub-directories,
and print results including mp3 tags to stdout or save as a CSV file
"""

# standard imports

# 3rd party imports
from tinytag import TinyTag

# local imports
import pfllib.PFLParams as PFLParams
import pfllib.PFLArgParse as PFLArgParse
import pfllib.PFLRun as PFLRun

class PFLRunMP3(PFLRun.PFLRun):
    def __init__(self, params):
        super().__init__(params)
        self.ColumnHeader = ["path", "filename", "length", "bitrate", "artist", "album", "track", "title", "year"]
        
    def handleMatch(self, match):
        try:
            tag = TinyTag.get(match)
            return [match.parent, match.name,
                    round(tag.duration,3), tag.bitrate,
                    tag.artist, "" if tag.album is None else tag.album.strip(),
                    tag.track, tag.title, tag.year]
        except:
            return [match.parent, match.name,
                    "", "", "", "", "", "" , ""]
            
class PFLParamsMP3(PFLParams.PFLParams):
    def __init__(self, scandir, recurse, outfile, outexistsmode, nodots):
        super().__init__("*.mp3", scandir, recurse, outfile, outexistsmode, nodots)
        
# define and collect commandline arguments
parser = PFLArgParse.PFLArgParseFixedPattern(description="List mp3 files in a directory and its sub-directories\n"
                                             + "and print results including mp3 tags to stdout or save as a CSV file.")
args = parser.parse_args()

try:
    # create parameter object
    params = PFLParamsMP3(args.scandir, args.recurse, args.outfile,
                          args.overwrite + args.append, args.nodots)

    print("Search for mp3 files in directory '{}'...".format(params.ScanPath))

    run = PFLRunMP3(params)
    
    run.Run()
except (Exception) as e:
    print("Unhandled error:", e.args[0])
