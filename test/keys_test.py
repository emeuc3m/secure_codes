#!/usr/bin/env python3
import pyminizip as pyzip
import json
from os import getcwd
import os
import shutil as sh


def zip_keys(username, password):
    """
    Arguments: username, password
    Returns: None
    """
    a = getcwd()
    source_path = getcwd() + "/test/keys"
    # source_path = getcwd() + "/db/" + username + "/" + "keys" #./db/username/keys.json
    
    destination_path = getcwd() + "/test/" "keys.zip" #./db/username/username_keys.zip
    compression = 8
    pyzip.compress(source_path, None, destination_path, password, compression)
    os.remove(source_path)
    os.chdir(a)
    return

if __name__ == '__main__':
    zip_keys("a", "1234")