import sqlite3
import csv

# DOCUMENTATION
# ==========================================================================
# Database Schema:
#     userdata      | username TEXT | password TEXT | email    TEXT |
#     story_content | username TEXT | storyID  INT  | content  TEXT | sequence INT  |
#     story_id      | storyID  INT  | title    TEXT |
#
# database connect()
# precond: database is not open
# postcond: connects to database and returns the database object
#
# void disconnect()
# precond: database is open
# postcond: takes a database object, saves it, and closes it
#
# void init() 
# precond:
# postcond: creates tables in database if they don't already exist
#
# int add_user (String username, String password, String email)
# precond: inputs are sanitized
# postcond: inserts the appropriate data into the userdata database
#           returns  0 if successful
#                   -1 if unsuccessful
#
# int add_story (String username, String title, String content)
# precond: inputs are sanitized, content is less than 200 chars
# postcond: inserts the appropriate data in the story_content database
#           returns  0 if successful
#                   -1 if unsuccessful
#
# boolean user_has_contributed (String username, int sid)
# precond: inputs are sanitized
# postcond: checks if a user has contributed to a story by sid
#           returns TRUE  if the user has contributed
#           returns FALSE if the user has not contributed
#           returns TRUE  if exception thrown
# 
# String get_story_title (int sid)
# precond: 
# postcond: returns corresponding story title given sid
#           if story does not exist, returns "<NO TITLE>"
# 
# ==========================================================================

# Table Editing Functions
# ==========================================================================
def connect():
    name = "./data/unencryptedpasswords.db"
    db = sqlite3.connect(name)
    c = db.cursor()
    return db

def disconnect(db):
    db.commit()
    db.close()

def init():
    db = connect()
    c = db.cursor()
    # Creating Tables
    cmd = "CREATE TABLE IF NOT EXISTS userdata (username TEXT, password TEXT, email TEXT)"
    c.execute(cmd)
    cmd = "CREATE TABLE IF NOT EXISTS story_content (username TEXT, storyID INTEGER, content TEXT, sequence INTEGER)"
    c.execute(cmd)
    cmd = "CREATE TABLE IF NOT EXISTS story_id (storyID INTEGER, title TEXT)"
    c.execute(cmd)
    disconnect(db)
    
def add_user(username, password, email):
    try:
        db = connect()
        c = db.cursor()
        req = "INSERT INTO userdata VALUES ('%s', '%s', '%s')"%(username,password,email)
        c.execute(req)
        disconnect(db)
        return "0"
    except:
        return "-1"

def add_story(username, title, content):
    try:
        db = connect()
        c = db.cursor()
        sid = largest_sid() + 1
        seq = largest_sequence(sid) + 1
        req = "INSERT INTO story_content VALUES ('%s', %s, '%s', %s)"%(username,sid,content,seq)
        c.execute(req)
        req = "INSERT INTO story_id VALUES (%s, '%s')"%(sid,title)
        c.execute(req)
        disconnect(db)
        return "0"
    except:
        return "-1"

def user_has_contributed(username, sid):
    try: 
        db = connect()
        c = db.cursor()
        req = "SELECT username FROM story_content WHERE storyID == %s"%(sid)
        ret = False
        data = c.execute(req)
        for entry in data:
            if entry[0] == username:
                ret = True
        disconnect(db)
        return ret
    except:
        return True 

def get_story_title(sid):
    try:
        db = connect()
        c = db.cursor()
        req = "SELECT title FROM story_id WHERE storyID == %s"%(sid)
        data = c.execute(req)
        ret = "NO TITLE"
        for entry in data:
            ret = entry[0] # Should be the only one
        disconnect(db)
        return ret
    except:
        return "NO TITLE"

# Table Accessing Functions
# ==========================================================================
def largest_sid():
    db = connect()
    c = db.cursor()
    req = "SELECT storyID FROM story_id"
    data = c.execute(req)
    maxSID = -1
    for entry in data: 
        if entry[0] > maxSID:
            maxSID = entry[0]
    disconnect(db)
    return maxSID

def largest_sequence(sid):
    db = connect()
    c = db.cursor()
    req = "SELECT sequence FROM story_content WHERE storyID == %s"%(sid)
    data = c.execute(req)
    maxSEQ = -1
    for entry in data: 
        if entry[0] > maxSEQ:
            maxSEQ = entry[0]
    disconnect(db)
    return maxSEQ

# Initialization
# ==========================================================================
if (__name__ == "__main__"):
    init()
