import sqlite3
from flask import Flask, url_for, redirect, render_template, session, request
from utils import content, auth, timestamp

app = Flask(__name__)
app.secret_key = "get to the choppa"

@app.route("/", methods=["POST","GET"])
def root():
    if request.method == "GET":
	if 'user' in session:
            # need to pass timestamp function
	    return render_template("stories.html", timestamp = timestamp.timestamp, usercontributed = content.get_user_stories(session['user']), usernotcontributed = content.get_no_user_stories(session['user']) )
	else: 
	    return render_template("home.html")
    else:
	return logreg() #user must be logged out (no forms in stories.html)
    
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

    login_num = auth.login(u,p)
    if login_num == 0:
        #print "logged in"
	session['user'] = u
	return render_template("stories.html", timestamp = timestamp.timestamp, usercontributed = content.get_user_stories(session['user']), usernotcontributed = content.get_no_user_stories(session['user']))
    elif login_num == 1:
	return render_template("home.html", message="Wrong password") 
    elif login_num == 2:	
	return render_template("home.html", message="Username isn't registered")
    
def reg():
    u = request.form['username']
    p = request.form['password']
    if (u == "" or p == ""):
	return render_template("home.html", message="You can't leave a field blank")

    reg_num = auth.register(u,p)
    if reg_num == 0:
	return render_template("home.html", message="Successfully registered!")
    elif reg_num == 1:
	return render_template("home.html", message="That username is already registered")
    
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
	cont = request.form["content"]

        title = title[0].upper() + title[1:]
        cont = cont[0].upper() + cont[1:]
        
        #print request.form
	if title == "":
            return render_template("new.html", message="You can't leave a field blank")
        if cont == "":
	    return render_template("new.html", message="You can't leave a field blank")
	u = session['user']
	content.add_story(u,title,cont)
	return redirect("/s/" + str(content.largest_sid()))
    
@app.route("/s/<int:sid>/", methods=["POST", "GET"])
def story(sid):
    if not content.sid_exists(sid):
        return redirect("/")
    if request.method == "GET":
	if 'user' in session:
            has_contrib = content.user_has_contributed(session['user'], sid)
	    return render_template("story.html", title = content.get_story_title(sid), story = content.get_contributions(sid), contributors = content.get_contributors(sid), timestamps = [timestamp.timestamp(d) for d in content.get_timestamps(sid)], contrib=has_contrib)
	else:
	    return redirect(url_for("root"))
    else: #adding an entry w/ POST
        #print request.form 
	cont = request.form["content"]
	u = session['user']
        content.extend_story(u, sid, cont)
        #print content.get_story_full(sid)
	return render_template("story.html", title=content.get_story_title(sid), story=content.get_contributions(sid), contributors = content.get_contributors(sid), timestamps = [timestamp.timestamp(d) for d in content.get_timestamps(sid)], contrib=True)
    
if __name__ == "__main__":
    app.debug = True
    app.run()


        
