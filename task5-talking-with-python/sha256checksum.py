"""
usage: sha256checksum.py [-h] server volume dir

Prints out the sha256 checksum of all files in the dir and subdirs.

positional arguments:
  server      The IP/Hostname of the server.
  volume      Gluster volume name inside the Host.
  dir         Path to the directory for whose subfiles you want to get the
              sha256 checksum.

optional arguments:
  -h, --help  show this help message and exit

"""


import hashlib
import os
from gluster import gfapi
import sys


def get_volume(server_name, volume_name):
    """Gets the volume from a host.
    
    Arguments:
        server_name {string} -- IP/Hostname of the server.
        volume_name {string} -- Gluster volume name inside the Host.
    
    Returns:
        [gluster.gfapi.gfapi.Volume] -- Mounted volume from the server.
    """

    volume = gfapi.Volume(server_name, volume_name)
    volume.mount()
    return volume

def find_check_sum_entire_directory(volume, path):
    """Prints the sha256 checksum of all the files contained in the path.
    
    Arguments:
        volume {gluster.gfapi.gfapi.Volume} -- The volume in which to open the path.
        path {string} -- Path to the directory for whose subfiles you want to get the sha256 checksum.
    """

    def find_check_sum_entire_directory_helper(path):

        if volume.isdir(path):
            for sub_path in volume.listdir(path):
                find_check_sum_entire_directory_helper(os.path.join(path,sub_path))

        if volume.isfile(path):
            with volume.fopen(path,"rb") as f:
                bytes = f.read()
                readable_hash = hashlib.sha256(bytes).hexdigest()
                print path + " " + readable_hash

    find_check_sum_entire_directory_helper(path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Prints out the sha256 checksum of all files in the dir and subdirs.')
    parser.add_argument('server', 
                        help='The IP/Hostname of the server.')

    parser.add_argument('volume',
                        help='Gluster volume name inside the Host.')
    
    parser.add_argument('dir',
                        help='Path to the directory for whose subfiles you want to get the sha256 checksum.')

    args = vars(parser.parse_args())
    volume = get_volume(args['server'], args['volume'])
    find_check_sum_entire_directory(volume, args['dir'])
