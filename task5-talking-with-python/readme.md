```
usage: sha256checksum.py [-h] server volume dir

Prints out the sha256 checksum of all files in the dir and subdirs.

positional arguments:
  server      The IP/Hostname of the server.
  volume      Gluster volume name inside the Host.
  dir         Path to the directory for whose subfiles you want to get the
              sha256 checksum.

optional arguments:
  -h, --help  show this help message and exit
```

Made using python2.7.
