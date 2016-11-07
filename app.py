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

    login_num = auth.login(u,p)
    if login_num == 0:
        print "logged in"
	session['user'] = u
	return render_template("stories.html", usercontributed = content.get_user_stories(session['user']), usernotcontributed = content.get_no_user_stories(session['user']))
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
	return render_template("home.html", message="Successfully registered")
    elif reg_num == 1:
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
	cont = request.form["content"]
        print request.form
	if title == "":
            return render_template("new.html", message="You can't leave a field blank")
        if cont == "":
	    return render_template("new.html", message="You can't leave a field blank")
	u = session['user']
	content.add_story(u,title,cont)
	return redirect("/s/" + str(content.largest_sid()))
    
@app.route("/s/<int:sid>/", methods=["POST", "GET"])
def story(sid):
    if request.method == "GET":
	if 'user' in session:
	    if content.user_has_contributed(session['user'], sid):
                print content.get_story_full(sid)
		return render_template("story.html", title = content.get_story_title(sid), story = content.get_story_full(sid), contrib=True)
	    else:
                print "notcont"
		return render_template("story.html",title = content.get_story_title(sid), story = content.get_story_last(sid), contrib=False)
	else:
	    return redirect(url_for("root"))
    else: #adding an entry w/ POST
        print request.form 
	cont = request.form["content"]
	if cont == "":
	    return render_template("story.html", message="You can't leave this field blank", title=content.get_story_title(sid), story = content.get_story_last(sid), contrib=False)
	u = session['user']
	content.extend_story(u, sid, cont)
        print content.get_story_full(sid)
	return render_template("story.html", title=content.get_story_title(sid), story=content.get_story_full(sid), contrib=True)
    
if __name__ == "__main__":
    app.debug = True
    app.run()


        
