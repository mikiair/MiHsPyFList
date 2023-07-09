# MiHsPyFList
Sort of a finger exercise in [Python](https://www.python.org) - several tools for listing files filtered by name/type in a folder and writing information to `stdout`, a CSV file or to a [Sqlite](https://www.sqlite.org) database.
* **pfl** - Simple file listing with just path and filename
* **pfli** - File listing with additional file information on size and creation / last write dates
* **pflh** - as before, plus SHA256 hash
* **pflj** - File listing with fixed search pattern '*.jpg', JPG width and height are written
* **pfl3** - File listing with fixed search pattern '*.mp3', MP3 tag information is given
* **pfl4** - File listing with fixed search pattern '*.mp4', MP4 tag information is given

## Usage
```pfl [-h] [-r] [-o | -a] [-n | -d DOTS] [pattern] [scandir] [outfile]```
### Positional arguments
  * pattern - only files matching this pattern will be listed
  * scandir - directory to scan for files (default=current folder)
  * outfile - CSV or database file to write results to (default=stdout)

### Optional arguments
  * -h, --help - show help message and exit
  * -r, --recurse - recurse sub-folders
  * -l, --limit - limit the scanned file size for hash value calculation to 100MB (**pflh** only)

### File options
  optional arguments apply when writing to CSV or database file (ignored otherwise)
  * -o, --overwrite - overwrite the outfile if existent
  * -a, --append - append to the outfile if existent
  * -n, --nodots - do not display dots for matches
  * -d DOTS, --dots DOTS - logarithmic number of matching files to display one dot for (i.e. 0=every file, 1=each 10 files, 2=each 100 files...)

## Requirements
For using the tools which log media file (jpg/mp3/mp4) properties, you will have to install one or more additional Python libraries:
* [TinyTag](https://pypi.org/project/tinytag/): used for **pfl3** and **pfl4**
```
pip install tinytag
```
* [Pillow](https://pillow.readthedocs.io/en/stable/installation.html): used for **pflj**
```
pip install Pillow
```
