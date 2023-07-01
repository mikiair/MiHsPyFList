# MiHsPyFList
Sort of a finger exercise in [Python](https://www.python.org) - several tools for listing files filtered by name/type in a folder and writing information to `stdout`, a CSV file or to a [Sqlite](https://www.sqlite.org) database.
* pfl - Simple file listing with just path and filename
* pfli - File listing with additional file information on size and creation / last write dates
* pfli5 - as before, plus MD5 hash
* pflj - File listing with fixed search pattern '*.jpg', JPG width and height are written
* pfl3 - File listing with fixed search pattern '*.mp3', MP3 tag information is given
* pfl4 - File listing with fixed search pattern '*.mp4', MP4 tag information is given
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
