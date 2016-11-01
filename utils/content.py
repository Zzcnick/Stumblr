import sqlite3
import csv

# Creating Database
name = "../data/unencryptedpasswords.db"
db = sqlite3.connect(name)
c = db.cursor()

# Creating Tables
cmd = "CREATE TABLE IF NOT EXISTS userdata (username TEXT, password TEXT, email TEXT)"
c.execute(cmd);
cmd = "CREATE TABLE IF NOT EXISTS story_content (username TEXT, storyID INTEGER, content TEXT, sequence INTEGER)"
c.execute(cmd);
cmd = "CREATE TABLE IF NOT EXISTS story_id (storyID INTEGER, title TEXT)"
c.execute(cmd);

# DOCUMENTATION
# ==========================================================================
# int insert_user (String username, String password, String email)
# precond: inputs are sanitized
# postcond: inserts the appropriate data into the userdata database
#           returns  0 if successful
#                   -1 if unsuccessful
#
# int insert_story (String username, String content)
# precond: inputs are sanitized, content is less than 200 chars
# postcond: inserts the appopriate data in the story_content database
#           returns  0 if successful
#                   -1 if unsuccessful
#  
#
#
#
#
#
#
#
#
#
#
#
#
# ==========================================================================

# Table Editing Functions
# ==========================================================================
def insert_user(username, password, email):
    try:
        req = "INSERT INTO userdata VALUES ('%s', '%s', '%s')"%(username,password,email)
        c.execute(req)
        return 0
    except:
        return -1

def insert_story(username, content):
    try:
        sid = get_last_story + 1
        seq = get_sequence(sid) + 1
        req = "INSERT INTO story_content VALUES ('%s', %s, '%s', %s)"%(username,sid,content,seq)
        c.execute(req)
        return 0
    except:
        return -1


# Table Accessing Functions
# ==========================================================================
def get_last_story():
    req = "SELECT storyID FROM story_id"
    
