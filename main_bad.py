#!/usr/bin/env python3

import atexit
import file_manager as fm
import security as sec
from getpass import getpass
import random, string, signal, sys, time
import os

# In case of a sigint or sigstp, encrypt the user's keys before exiting.
@atexit.register
def encrypt_keys():
    global a, b
    try:
        fm.zip_keys(a,b)
        del a, b
    except NameError:
        pass
    print("Exiting...")
    sys.exit(0)
        


class App:
    def __init__(self):
        self.user = None
        self.password = None

        db_dir = os.getcwd() + "/db"
        
        if not os.path.exists(db_dir):
            fm.make_dir(db_dir)
            fm.create_database(db_dir)
    
    def create_user(self):
        """
        Asks for a username that does not exists and a password and creates that user, 
        meaning it add the needded information (username, hashed password and user id) to the database and creates a directory with the username
        Argument: None
        Returns: None
        """
        
        username = input("Enter your username: ") # ask for a username
        while fm.user_exists(username): # loops if username exists in teh database
            username = input("Username already exists, enter a new one: ") # if th euser already exists ask for a new one

        # when the function arrives here we know that the username isnt repeated
        
        id = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) # assign the user a random string
        password = getpass() # ask for a password
        password_hash = sec.hash(password + id) # hash the password with the id appended so that two equal passwords do not have the same hash output
        data_to_dump = {"password": password_hash,"id": id} # creates the data with the username, password and id to add to the database

        fm.update_json(username, data_to_dump) #updates the database
        upath = "./db/" + username # sets the path for the user directory
        fm.make_dir(upath) # reates the directory
        fm.initial_key_zip(username,password)
        
        return
        

    def login(self):
        """
        Asks for a username that already exists and for the password of the user, if they math it returns True
        Argument: None
        Returns: True
        """
        print("\033[92m") # \033[92m = green
        print("-----------------------------------------")
        print("----------------- LOGIN -----------------") 
        print("-----------------------------------------")
        print("\033[0m") # \033[0m default console color
        username = input("Enter your username (enter x to exit): ") #asks for the username
        while not fm.user_exists(username): #loops if the username does not exist
            username = input("Username does not exists, enter a new one (enter x to exit): ") #if the entered username does not exist it asks for it again
            if username == "x":
                return False
            
        #when the function arrives here we know that the enterez username exists
        data = fm.load_db()
        id = data[username]["id"] #get user id

        password = getpass() #asks for the pasword
        hpassword = sec.hash(password + id) #hashes the password with the id
        jsonpassword = data[username]["password"]

        while hpassword != jsonpassword: #checks if the entered password is the same as the one in the database (checks the hashes)
            print("Incorrect password, try again.")
            password = getpass() #asks for the pasword again
            hpassword = sec.hash(password + id) #hashes the password with the id again


        fm.unzip_keys(username, password)

        global a, b
        self.user = a = username
        self.password = b = password

        
        print(f"\033[4mWelcome, {self.user}! \033[0m")


        return True

    def upload_file(self, path):
        # read
        # encrypt
        # save in zip and encrypted file in db

        # Extract the name of the file in linux based OS 
        if os.name == "posix":
            name = path.split("/")[-1]
        # Extract the name of the file in windows 
        elif os.name == "nt":
            name = path.split("\\")
        
        # Check that the file has not been uploaded
        dir_path = os.getcwd() + "/db/" + self.user + "/" # get the path for the username database
        files_in_dir = os.listdir(dir_path) 
        if name in files_in_dir:
            print("A file with the same name already exists, please change the name.")
            return
            
        # Encrypt
        encription_info = sec.sim_encrypt_file(path)
        if encription_info == -1:
            print("File does not exist.")
            return

        for x in range(1, 100):
            time.sleep(0.01)
            print("Uploaded: " + str(x) +"%", end="\r")
        print("Uploaded: 100%\n")

        # Save the encryption info
        fm.save_encryption(self.user, name, encription_info) # x=username (global variable)

        return

    def download_file(self):
        # Show files 
        user_files = fm.get_files(self.user) 
        file_name = False
        if len(user_files) == 0:
            print("There are no uploaded files.")
            return
        file_found = False
        while not file_found:
            file_name = input(f"Uploaded files: {user_files}\nSelect file: ")
            if file_name not in user_files:
                print("File does not exist.")
            else:
                file_found = True
                
        
        print("Downloading file: " + file_name + "...")
        for x in range(1, 100):
            time.sleep(0.02)
            print("Downloaded: " + str(x) +"%", end="\r")
        print("Downloaded: 100%\n")
        
        # Search file in database
        encription_info = fm.get_file_from_db(self.user, file_name)
        # Decrypt
        decrypted_data = sec.sim_decrypt_file(encription_info[0], encription_info[1], encription_info[2], encription_info[3])
        # save the decrypted data in a file
        fm.save_file(self.user, file_name, decrypted_data)
        
        return

    
    def exit_app(self, errorcode=0):
        print("Exiting...")
        if self.user is not None:
            fm.zip_keys(self.user,self.password)
            del self.user, self.password
        sys.exit(errorcode)

    def main(self):
        print("-------------------------------------------------------------------------------------------------------------------------------")
        print("WARNING: TO EXIT DO NOT USE CTRL+D, IT WILL CRASH THE DATABASE\nPlease use ctrl+c or ctrl+z instead\nIf ctrl+d was pressed, to fix it, run the file 'file_manager.py, this will reset the database deleting everything inside of it")
        print("-------------------------------------------------------------------------------------------------------------------------------")        
        logged = False
        while not logged:
            msg = input("Create user [c], Login [l], Exit[x]: ")

            if msg.lower() == "c":
                self.create_user()
                logged = self.login()

            elif msg.lower() == "l":
                logged = self.login()

            elif msg.lower() == "x":
                self.exit_app()
                
            else:
                print("Invalid input, please try again.")
        while True:
            msg = input("Upload File [u], Download File[d], Exit[x]: ")

            if msg.lower() == "u":
                path = input("Specify file path: ")
                self.upload_file(path)
                
            elif msg.lower() == "d":
                self.download_file()
            
            elif msg.lower() == "x":
                self.exit_app()
            
            else:
                print("Invalid input, please try again.")
            




if __name__ == '__main__':
    App().main()
