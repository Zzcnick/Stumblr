import sqlite3
import csv

# DOCUMENTATION
# ==========================================================================
# Database Schema:
#     userdata      | username TEXT | password TEXT |
#     story_content | username TEXT | storyID  INT  | content  TEXT | sequence INT  |
#     story_id      | storyID  INT  | title    TEXT |

# database connect()
# precond: database is not open
# postcond: connects to database and returns the database object

# void disconnect()
# precond: database is open
# postcond: takes a database object, saves it, and closes it

# void init() 
# precond:
# postcond: creates tables in database if they don't already exist

# void reset()
# precond: tables in database exist (init() has been previously called)
# postcond: clears all entries in the database

# boolean add_user (String username, String password)
# precond: inputs are sanitized
# postcond: inserts the appropriate data into the userdata database
#           returns TRUE  if successful
#                   FALSE if unsuccessful

# boolean add_story (String username, String title, String content)
# precond: inputs are sanitized, content is less than 200 chars
# postcond: inserts the appropriate data in the story_content database
#           returns TRUE  if successful
#                   FALSE if unsuccessful

# boolean extend_story (String username, int sid, String content)
# precond: inputs are sanitized, content is less than 200 chars
# postcond: inserts the content into the appropriate story
#           returns TRUE  if successful
#           returns FALSE if unsuccessful

# boolean user_has_contributed (String username, int sid)
# precond: inputs are sanitized
# postcond: checks if a user has contributed to a story by sid
#           returns TRUE  if the user has contributed
#           returns FALSE if the user has not contributed
#           returns TRUE  if exception thrown

# String get_story_title (int sid)
# precond: 
# postcond: returns corresponding story title given sid
#           if story does not exist, returns "NO TITLE"

# String get_story_last (int sid)
# precond: 
# postcond: returns latest update to a story given sid
#           if story does not exist, returns "NO CONTENT"

# [ [ int, String, [String, ...], [String, ...]  ] ... ] get_user_stories (String username) 
# precond: 
# postcond: returns all the stories a user has contributed to
#           in a 2D array where each entry's index 0 is the sid
#                                            index 1 is the title
#                                            index 2 is the list of contributions
#                                            index 3 is the list of users who contributed to the story
#           returns an empty array if no such stories

# [ [ int, String, [String, ...], [String, ...] ] ... ] get_no_user_stories (String username) 
# precond: 
# postcond: returns all the stories a user hasn't contributed to
#           in a 2D array where each entry's index 0 is the sid
#                                            index 1 is the title
#                                            index 2 is the list of contributions
#                                            index 3 is the list of users who contributed to the story
#           returns an empty array if no such stories

# [ String, ... ] get_contributors (int sid)
# precond:
# postcond: returns an array of contributors to the post with sid
#           each index of the array corresponds to the corresponding sequence number
#           of the addition in the db

# [ String, ... ] get_contributions (int sid)
# precond:
# postcond: returns an array of contributions to the post with sid
#           each index of the array corresponds to the corresponding sequence number
#           of the addition in the db

# int largest_sid()
# precond:
# postcond: returns largest sid in database
#           if no stories in database, returns -1

# int largest_sequence (int sid)
# precond: 
# postcond: returns largest sequence for a given sid
#           if sid does not exist, returns -1

# boolean sid_exists (int sid)
# precond:
# postcond: returns TRUE  if sid exists in database
#           returns FALSE otherwise

# String get_title (int sid)
# precond:
# postcond: returns title of story with corresponding sid
#           if story does not exist, returns "NO TITLE"
# ==========================================================================

# Table Editing Functions
# ==========================================================================
def connect():
    name = "./data/unencryptedpasswords.db"
    db = sqlite3.connect(name)
    return db

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

def reset():
    db = connect()
    c = db.cursor()
    # Delete Entries
    cmd = "DELETE FROM userdata"
    c.execute(cmd)
    cmd = "DELETE FROM story_content"
    c.execute(cmd)
    cmd = "DELETE FROM story_id"
    c.execute(cmd)
    disconnect(db)
    
def add_user(username, password):
    try:
        db = connect()
        c = db.cursor()
        req = "INSERT INTO userdata VALUES (?,?)"
        c.execute(req, (username,password))
        disconnect(db)
        return True
    except:
        return False

def add_story(username, title, content):
    try:
        db = connect()
        c = db.cursor()
        sid = largest_sid() + 1
        req = "INSERT INTO story_content VALUES (?,?,?,?)"
        c.execute(req, (username, sid, content, 0))
        req = "INSERT INTO story_id VALUES (?,?)"
        c.execute(req, (sid, title))
        disconnect(db)
        return True
    except:
        return False

def extend_story(username, sid, content):
    try: 
        db = connect()
        c = db.cursor()
        ret = False
        if (sid_exists(sid) and not user_has_contributed(username, sid)):
            #print "sid_exists"
            seq = largest_sequence(sid) + 1
            #print "sid2"
            req = "INSERT INTO story_content \
                   VALUES (?,?,?,?)"
            c.execute(req, (username, sid, content, seq))
            #print "sid3"
            ret = True
        disconnect(db)
        return ret
    except:
        return False

def user_has_contributed(username, sid):
    try: 
        db = connect()
        c = db.cursor()
        req = "SELECT username FROM story_content WHERE storyID == ?"
        ret = False
        data = c.execute(req, (sid,))
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
        req = "SELECT title FROM story_id WHERE storyID == ?"
        data = c.execute(req, (sid,))
        ret = "NO TITLE"
        for entry in data:
            ret = entry[0] # Should be the only one
        disconnect(db)
        return ret
    except:
        return "NO TITLE"

def get_story_last(sid):
    try:
        maxSEQ = largest_sequence(sid)
        db = connect()
        c = db.cursor()
        req = "SELECT content \
               FROM story_content \
               WHERE storyID == ? and sequence = ?"
        data = c.execute(req, (sid, maxSEQ))
        ret = "NO CONTENT"
        for entry in data:
            ret = entry[0] # Should be the only one
        disconnect(db)
        return ret
    except:
        return "NO CONTENT"

def get_story_full(sid):
    try:
        db = connect()
        c = db.cursor()
        req = "SELECT sequence, content \
               FROM story_content \
               WHERE storyID == ? \
               ORDER BY sequence"
        data = c.execute(req, (sid,))
        retSTR = ""
        for entry in data:
            retSTR += entry[1].strip() + " "
        disconnect(db)
        return retSTR
    except: 
        return "ERROR"

def get_user_stories(username):
    try:
        db = connect()
        c = db.cursor()
        req = "SELECT story_id.storyID, story_id.title \
               FROM story_id, story_content \
               WHERE story_content.username == ? \
                 and story_id.storyID == story_content.storyID \
               ORDER BY story_id.storyID"
        data = c.execute(req, (username,))
        ret = []
        for entry in data:
            ret += [[ entry[0], entry[1], get_contributions(entry[0]), get_contributors(entry[0]) ]]
        disconnect(db)
        return ret
    except: 
        return []

def get_no_user_stories(username):
    try:
        db = connect()
        c = db.cursor()
        req = "SELECT story_id.storyID, title, story_content.username \
               FROM story_id, story_content \
               WHERE story_id.storyID == story_content.storyID"
        data = c.execute(req)
        indices = range(0, largest_sid() + 1) # storyIDs
        for entry in data:
            if entry[2] == username:
                indices[entry[0]] = -1; # invalid storyIDs
        ret = []
        for i in indices:
            if i > 0: # valid storyIDs
                ret += [[ i, get_title(i), get_contributions(i), get_contributors(i) ]]
        disconnect(db)
        return ret
    except: 
        return []

# dev branch additional functions
# ==========================================================================
def get_contributors(sid):
    db = connect()
    c = db.cursor()
    req = "SELECT username FROM story_content WHERE storyID=? ORDER BY sequence"
    c.execute(req, (sid,))
    ret = [uname[0] for uname in c.fetchall()]
    return ret

def get_contributions(sid):
    db = connect()
    c = db.cursor()
    req = "SELECT content FROM story_content WHERE storyID=? ORDER BY sequence"
    c.execute(req, (sid,))
    ret = [cont[0] for cont in c.fetchall()]
    return ret    

# Table Accessing Functions
# ==========================================================================
def largest_sid():
    db = connect()
    c = db.cursor()
    req = "SELECT storyID FROM story_id"
    data = c.execute(req)
    maxSID = 0
    for entry in data: 
        if entry[0] > maxSID:
            maxSID = entry[0]
    disconnect(db)
    return maxSID

def largest_sequence(sid):
    db = connect()
    c = db.cursor()
    req = "SELECT sequence FROM story_content WHERE storyID == ?"
    data = c.execute(req, (sid,))
    maxSEQ = -1
    for entry in data: 
        if entry[0] > maxSEQ:
            maxSEQ = entry[0]
    disconnect(db)
    return maxSEQ

def sid_exists(sid):
    db = connect()
    c = db.cursor()
    req = "SELECT storyID FROM story_id WHERE storyID == ?"
    c.execute(req, (sid,))
    if c.fetchone():
        return True
    return False

def get_title(sid):
    db = connect()
    c = db.cursor()
    req = "SELECT title FROM story_id WHERE storyID == ?"
    data = c.execute(req, (sid,) )
    ret = "NO TITLE"
    for entry in data:
        ret = entry[0]
    disconnect(db)
    return ret;

# Initialization
# ==========================================================================
if (__name__ == "__main__"):
    init()
