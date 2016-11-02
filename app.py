from flask import Flask
from utils import content, auth
app = Flask(__name__)

@app.route("/test/")
def test():
    return content.insert_user("test", "not hashed", "lol")

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
#    if 

app.run()
