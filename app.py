import sqlite3
import csv
from flask import Flask,url_for,redirect,render_template,session
from utils import content, auth
app = Flask(__name__)

# Initializing Database
# ==========================================================================
'''
name = "./data/unencryptedpasswords.db"
db = sqlite3.connect(name)
c = db.cursor()
cmd = "CREATE TABLE IF NOT EXISTS userdata (username TEXT, password TEXT, email TEXT)"
c.execute(cmd);
cmd = "CREATE TABLE IF NOT EXISTS story_content (username TEXT, storyID INTEGER, content TEXT, sequence INTEGER)"
c.execute(cmd);
cmd = "CREATE TABLE IF NOT EXISTS story_id (storyID INTEGER, title TEXT)"
c.execute(cmd);
'''
# ==========================================================================

@app.route("/test/")
def test():
    return content.insert_user("this", "is", "saddening")

@app.route("/")
def authenticate():
    if user in session:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

@app.route("/login", methods = ["POST"])
def auth():
    if 'login' in request.form:
        return login()
    else:
        return reg()

def login():
    u = request.form['username']
    p = request.form['password']
    if auth.login(u,p) == "":
        session['user'] = p
        return redirect(url_for("authenticate"))  

app.debug = True
app.run()
