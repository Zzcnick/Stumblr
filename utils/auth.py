#Stumblr - auth.py
#Authentication Module
#Written by Misha

import sqlite3, hashlib

#Login Function
#boolean login(username [str], password [str])
def login(username, password):
    db = connect()
    c = db.cursor()
    req = "SELECT username FROM userdata WHERE username == ?"
    c.execute(req, (username,))
    if c.fetchone(): #if registered
        pass_field = "SELECT password FROM userdata WHERE username == ?"
        
        c.execute(pass_field, (username,))
        hashed_pass = hashlib.sha384(password).hexdigest()
        db_hashed_pass = c.fetchone()[0]

        if hashed_pass == db_hashed_pass:
            return 0 #successful
        else:
            return 1 #wrong password
    else:
        return 2 #user doesnt exist
        
    
#Register Function
#boolean register(username [str], password [str])
def register(username, password):
    db = connect()
    c = db.cursor()
    req = "SELECT username FROM userdata WHERE username == ?"
    c.execute(req, (username,))
    if not c.fetchone():
        req = "INSERT INTO userdata VALUES (?, ?)"
        c.execute(req, (username, hashlib.sha384(password).hexdigest()))
        disconnect(db)
        return 0
    else:
        return 1 #user already exists


#=====CONNECTION FUNCTIONS=====#

#Connection connect()
def connect():
    name = "./data/unencryptedpasswords.db"
    db = sqlite3.connect(name)
    c = db.cursor()
    return db

#void disconnect(db [Connection])
def disconnect(db):
    db.commit()
    db.close()

def init():
    db = connect()
    c = db.cursor()
    # Creating Tables
    cmd = "CREATE TABLE IF NOT EXISTS userdata (username TEXT, password TEXT)"
    c.execute(cmd)
    cmd = "CREATE TABLE IF NOT EXISTS story_content (username TEXT, storyID INTEGER, content TEXT, sequence INTEGER)"
    c.execute(cmd)
    cmd = "CREATE TABLE IF NOT EXISTS story_id (storyID INTEGER, title TEXT)"
    c.execute(cmd)
    disconnect(db)

    
if (__name__ == "__main__"):
    init()
