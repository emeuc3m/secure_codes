import os
import json

db_path = os.getcwd() + "/test/testdb.json"
db = open(db_path, "rb")
keys = {}
encrypted_messages = []
decrypted_messages = []


db_dict = json.load(db)
unread = 0
for x in db_dict:
    for y in db_dict[x]:
        unread += 1
        print(db_dict[x][y])


def get_messages(usr):
    key_dict = usr + "sym_key"
    key = keys[key_dict]
    for x in db_dict[usr]:
        encrypted_messages.append(db_dict[usr][x])
        decrypted_messages.append(hybrid.decrypt(db_dict[usr][x], key[a], key[b], key[c]))

#decrypt part
for x in db_dict:
    get_messages(x)



print(unread)
