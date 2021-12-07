#!/usr/bin/env python3
import pyminizip as pyzip
import json
from os import getcwd
import os
import shutil as sh
import security as sec


def zip_keys(username, password):
    """
    Arguments: username, password
    Returns: None
    """
    a = getcwd()
    source_path = getcwd() + "/db/" + username + "/" + "keys.json" #./db/username/keys.json
    destination_path = getcwd() + "/db/" + username + "/" + username + "_keys.zip" #./db/username/username_keys.zip

    rsa_key_path = getcwd() + "/db/" + username + "/" + "private.pem"
    rsa_key_destination_path = getcwd() + "/db/" + username + "/" + "private.zip"

    messages_path = getcwd() + "/db/" + username + "/" + "read_messages.json"
    messages_destination_path = getcwd() + "/db/" + username + "/" + "read_messages.zip"

    compression = 8
    pyzip.compress(source_path, None, destination_path, password, compression)
    pyzip.compress(rsa_key_path, None, rsa_key_destination_path, password, compression)
    pyzip.compress(messages_path, None, messages_destination_path, password, compression)
    os.remove(source_path)
    os.remove(rsa_key_path)
    os.remove(messages_path)
    os.chdir(a)
    return


def unzip_keys(username, password):
    """
    Arguments: username, password
    Returns: None
    """
    a = getcwd()
    source_path = getcwd() + "/db/" + username + "/" + username + "_keys.zip" #./db/username/username_keys.zip
    destination_path = getcwd() + "/db/" + username #./db/username/

    rsa_key_source_path = getcwd() + "/db/" + username + "/" + "private.zip"
    rsa_key_destination_path = getcwd() + "/db/" + username

    messages_source_path = getcwd() + "/db/" + username + "/" + "read_messages.zip"
    messages_destination_path = getcwd() + "/db/" + username

    # print(rsa_key_source_path)
    # print(rsa_key_destination_path)
    pyzip.uncompress(source_path, password, destination_path, 0)
    pyzip.uncompress(rsa_key_source_path, password, rsa_key_destination_path, 0)
    pyzip.uncompress(messages_source_path, password, messages_destination_path, 0)
    os.remove(source_path)
    os.remove(rsa_key_source_path)
    os.remove(messages_source_path)
    os.chdir(a)
    return

def main():
    # unzip_keys("user2", "1234")
    zip_keys("user2", "1234")


if __name__ == '__main__':
    main()