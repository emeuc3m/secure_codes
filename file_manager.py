#!/usr/bin/env python3
import pyminizip as pyzip
import json
from os import getcwd
import os
import shutil as sh
import security as sec

path = "./db/users.json"
#save and get from json with str

def make_dir(path):
    os.mkdir(path)
    return


def user_exists(username, path="./db/users.json"):
    exists = False # boolean variable that will turn to True if the username specified exists in the database
    with open(path, "r", encoding="utf-8", newline="") as database:
        users = json.load(database)
        database.close()
    if username in users:
        exists = True
    return exists
    
def get_number_of_elements(path):
    with open(path, "r", encoding="utf-8", newline="") as database:
        data = json.load(database)
        database.close()

    return len(data)
    
def send_message(username, message,sender):
    path = getcwd() + "/db/" + username + "/unread_messages.json"
    update_json(sender,message,path)

def check_handshake(user, destination):
    keys_path = getcwd() + "/db/" + user + "/keys.json"
    with open(keys_path, "r", encoding="utf-8", newline="") as database:
        keys = json.load(database)
        database.close()
    if not destination in keys:
        return False

    else:
        return True


def update_json(dict_key, data_to_dump, path = "./db/users.json"):
    """
    If the json doesn't exist, create it, otherwise include the new data in it.
    Argument: dict_key, data_to_dump
    Returns: None
    """
        # if database does not exist, create it
    if not os.path.exists(path):
        try:
            with open(path, "w", encoding="utf-8", newline="") as database:
                json.dump({dict_key: data_to_dump}, database, indent=2)
        except FileNotFoundError as ex:
            raise Exception("Wrong file or file path")
    else:
        reading_error = False
        try:
            with open(path, "r", encoding="utf-8", newline="") as database:
                data = json.load(database)
                
                # if the key is not in the database, add it
                if dict_key not in database:
                    data[dict_key] = data_to_dump

        # this prevents reading to an empty json file
        except Exception:
            reading_error = True
            with open(path, "w", encoding="utf-8", newline="") as database:
                json.dump({dict_key: data_to_dump}, database, indent=2)

        if not reading_error:
            # write the changes to the json file
            with open(path, "w", encoding="utf-8", newline="") as database:
                json.dump(data, database, indent=2)
        else:
            raise Exception("Error reading from JSON")
    return
    

def get_msg(user, index):
    path = getcwd() + "/db/" + user + "/unread_messages.json"

    with open(path, "r", encoding="utf-8", newline="") as json_file:
        data = json.load(json_file)
        json_file.close()
    id = list(data.keys())[index]
    return data[id]


    return

def index_in_json(index, path):
    with open(path, "r", encoding="utf-8", newline="") as json_file:
        data = json.load(json_file)
        json_file.close()
    try:
        ret = list(data.keys()).index(index)
    except ValueError:
        ret = -1
    return ret
        

def save_message(user, message, index):
    path = getcwd() + "/db/" + user + "/read_messages.json"
    with open(path, "r", encoding="utf-8", newline="") as json_file:
        data = json.load(json_file)
        json_file.close()

    

def delete_message(user, index, message):
    path = getcwd() + "/db/" + user + "/unread_messages.json"
    with open(path, "r", encoding="utf-8", newline="") as json_file:
        data = json.load(json_file)
        json_file.close()

    id = list(data.keys())[index]
    del data[id]

    with open(path, "w", encoding="utf-8", newline="") as json_file:
        json.dump(data, json_file)
        json_file.close()

    read_path = getcwd() + "/db/" + user + "/read_messages.json"
    with open(read_path, "r", encoding="utf-8", newline="") as json_file:
        read_data = json.load(json_file)
        json_file.close()

    sender = id.split("-")[0]

    try:
        messages_sender = read_data[sender]
        keys = list(messages_sender.keys())
        # print(keys + "njoohjbjsjdj")
        new_key = int(keys[-1]) + 1


    except KeyError:
        messages_sender = {}
        new_key = 0

    # print(new_key, "mlnjnocno")
    messages_sender[str(new_key)] = message
    # print(messages_sender)
    update_json(sender, messages_sender, read_path)

    return sender

    

def get_content_json(path, key) -> dict:
    with open(path, "r", encoding="utf-8", newline="") as json_file:
        data = json.load(json_file)
        json_file.close()
    return data[key]

def initial_key_zip(username, password):
    """
    Creates a zip protected with the password in the user directory to store the keys
    Argument: username, password
    Returns: True/False
    """
    file_name = username + "_keys.zip"
    path = getcwd() + "/db/" + username + "/" + file_name
    kpath = "/tmp/keys.json"
    data = {}
    with open(kpath, "w", encoding="utf-8", newline="") as keys:
        json.dump(data,keys)
        keys.close()
    compression = 8
    pyzip.compress(kpath, None, path, password, compression)
    os.remove(kpath)
    return

def create_database(path):
    a = path + "/users.json"
    with open(a, "w+",encoding="utf-8", newline="") as test:
        json.dump({}, test)

def reset_database(path):
    """
    resets the database by eliminating all files and directories and recreating the users.json as an empty dictionary
    Arguments: path
    Returns: None
    """
    f = os.listdir(path)
    for x in f:
        try: sh.rmtree(path + "/" + x)
        except: os.remove(path + "/" + x)

    a = path + "/users.json"
    with open(a, "w+",encoding="utf-8", newline="") as test:
        json.dump({}, test)
    return


def load_db():
    with open(path, "r", encoding="utf-8", newline="") as database: #open the databas
        data = json.load(database) #load teh database
        database.close() #close the database
    return data



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

    pyzip.uncompress(source_path, password, destination_path, 0)
    pyzip.uncompress(rsa_key_source_path, password, rsa_key_destination_path, 0)
    pyzip.uncompress(messages_source_path, password, messages_destination_path, 0)
    os.remove(source_path)
    os.remove(rsa_key_source_path)
    os.remove(messages_source_path)
    os.chdir(a)
    return

def add_enc_ext(file):
    splitted = file.split(".")
    n = len(splitted)
    file = ""
    for ii in range(n): # Get the name without the extension
        if ii == n-1:
            file +="_enc." + splitted[ii]
        else:
            file += splitted[ii]
    
    return file

def del_enc_ext(file):
    # Delete the "enc" from the name and substitute it by "downloaded"
    splitted = file.split("_")
    extension = splitted[-1].split(".") # ["enc", file extension]
    splitted[-1] = extension[1] # Change "enc.txt" for "txt"
    dec_name = ""
    n = len(splitted)
    for ii in range(n):
        if ii == n-1:
            dec_name += "_downloaded."+splitted[ii]
        elif ii==0:
            dec_name += splitted[ii]
        else:
            dec_name += "_"+splitted[ii]

    return dec_name
def save_encryption(username, name, encription_info: list): # ctext, key, tag, nonce
    name = add_enc_ext(name)

    dir_path = getcwd() + "/db/" + username + "/" + name # Hash this?? # path to the file with the encrypted data
    keys_path = getcwd() + "/db/" + username + "/keys.json" # file to the keys.zip to add the new encryption info

    # Add to the json the encription info"
    encription_data = {"a": encription_info[1], "b": encription_info[2], "c": encription_info[3]}
    update_json(sec.hash(name) , encription_data, keys_path)

    # Open file for the encrypted data and write it.
    with open(dir_path, "w", encoding="utf-8", newline="") as ctext_file:
        ctext_file.write(encription_info[0])
        ctext_file.close()
    return

def get_files(username):
    path = getcwd() + "/db/" + username
    excluded = "keys.json"
    files = os.listdir(path)
    files.remove(excluded)
    return files

def get_file_from_db(username, name):
    base_path = getcwd() + "/db/" + username +"/"
    file_path = base_path + name
    json_path = base_path + "keys.json"
    with open(file_path, "r", encoding="utf-8", newline="") as ctext_file:
        ctext = ctext_file.read()
    
    json_data = get_content_json(json_path, sec.hash(name))

    data = [ctext, json_data["a"], json_data["b"], json_data["c"]]
    
    return data

def delete_encription_data(username, name):
    json_path = getcwd() + "/db/" + username +"/keys.json"
    with open(json_path, "r", encoding="utf-8", newline="") as json_file:
        data = json.load(json_file)
        json_file.close()
    
    file_path = getcwd() + "/db/" + username +"/" + name
    os.remove(file_path)
    del data[sec.hash(name)]

    with open(json_path, "w", encoding="utf-8", newline="") as json_file:
        json.dump(data, json_file)
        json_file.close()
        
def save_file(username, name, data):
    dec_name = del_enc_ext(name)
    
    file_path = getcwd() + "/db/" + username +"/" + dec_name 
    delete_encription_data(username, name)
    with open(file_path, "w", encoding="utf-8", newline="") as text_file:
        text_file.write(data)
        text_file.close()
    return 


if __name__ == '__main__':
    # reset_database("./db")
    pass