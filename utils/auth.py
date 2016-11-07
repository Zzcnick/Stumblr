#Stumblr - auth.py
#Authentication Module
#Written by Misha

import sqlite3, hashlib

#Login Function
#int login(username [str], password [str])
def login(username, password):
    """
    Attempts to log in the given user by checking given credentials against
    the database, and reports on success.

    Args:
        username (str): username of user to log in
        password (str): password of user to log in

    Returns:
        int: 0 if successful, 1 if given and stored passwords don't match, 
            2 if username not in database
    """

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
#int register(username [str], password [str])
def register(username, password):
    """
    Attempts to register a user given a username and password,
    and reports on success.

    Args:
        username (str): username of user to register
        password (str): password of user to register

    Returns:
        int: 0 if successful, 1 if user already exists
    """
    
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
    """
    Helper function that opens a connection to the app's
    database, and returns a Connection object.

    Returns:
        Connection: sqlite3 conn object to database
    """
    
    name = "./data/unencryptedpasswords.db"
    db = sqlite3.connect(name)
    c = db.cursor()
    return db

#void disconnect(db [Connection])
def disconnect(db):
    """
    Helper function that commits to the database and closes
    the connection.

    Args:
        db (Connection): sqlite3 conn object to database
    """
    
    db.commit()
    db.close()

#void init()
def init():
    """
    Run only when this module is used as a standalone program,
    this module initalizes the database but checking for the tables required
    by the app, and creating them if they don't exist.
    """
        
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

#Specifies that the code is to be run only when program is standalone
if (__name__ == "__main__"):
    init()
