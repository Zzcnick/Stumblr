import sqlite3
from flask import Flask,url_for,redirect,render_template,session, request
from utils import content, auth

app = Flask(__name__)
app.secret_key = "get to the choppa"

@app.route("/", methods=["POST","GET"])
def root():
    if request.method == "GET":
	if 'user' in session: 
	    return render_template("stories.html", usercontributed = content.get_user_stories(session['user']), usernotcontributed = content.get_no_user_stories(session['user']))
	else: 
	    return render_template("home.html")
    else:
	return logreg() #user must be logged out (not forms in stories.html)
    
def logreg():
    if 'login' in request.form:
	return login()
    else:
	return reg()
    
def login():
    u = request.form['username']
    p = request.form['password']
    if (u == "" or p == ""):
	return render_template("home.html", message="You can't leave a field blank")
    if auth.login(u,p) == 0:
        print "logged in"
	session['user'] = u
	return render_template("stories.html")
    else:	
	return render_template("home.html", message="Wrong password and/or username")
    
def reg():
    u = request.form['username']
    p = request.form['password']
    if (u == "" or p == ""):
	return render_template("home.html", message="You can't leave a field blank")
    if auth.register(u,p) == 0:
	return render_template("home.html", message="Successfully registered")
    else:
	return render_template("home.html", message="Username is already registered")
    
@app.route("/logout/")
def logout():
    if 'user' in session:
	session.pop('user')
    return redirect(url_for("root"))
    
@app.route("/new/", methods =["POST", "GET"])
def new():
    if request.method == "GET":
	if 'user' in session:
	    return render_template("new.html")
	else:
	    return redirect(url_for("root"))
    else:
	title = request.form["title"]
	content = request.form["content"]
	if title == "" or content == "":
	    return render_template("new.html", message="Can't leave a field blank")
	u = session['user']
	content.addstory(u,title,content)
	return redirect(url_for("root"))
    
@app.route("/s/<int:sid>/")
def story(sid):
    if request.method == "GET":
	if 'user' in session:
	    if content.user_has_contributed(sid):
		return render_template("story.html", story = content.get_story_full(sid), contrib=True)
	    else:
		return render_template("story.html",story = content.get_story_last(sid), contrib=False)
	else:
	    return redirect(url_for("root"))
    else: #adding an entry w/ POST
	content = request.form["content"]
	if content == "":
	    return render_template("story.html", message="Can't leave this field blank", story = content.get_story_last(sid), contrib=False)
	u = session['user']
	# append entry to database
	return render_template("story.html", content.get_story_full(sid), contrib=True)
    
if __name__ == "__main__":
    app.debug = True
    app.run()


        
