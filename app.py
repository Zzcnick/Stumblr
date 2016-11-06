Bimport sqlite3
from flask import Flask,url_for,redirect,render_template,session
from utils import content, auth
app = Flask(__name__)
app.secretkey = 
@app.route("/test/")
def test():
    return content.insert_user("this", "is", "saddening")

@app.route("/")
def authenticate():
    if user in session:
        return redirect(url_for("home"))
    else:
        return redirect(reder_template("login.html"))

@app.route("/login/", methods = ["POST"])
def auth():
    if 'login' in request.form:
        return login()
    else:
        return reg()

def login():
    u = request.form['username']
    p = request.form['password']
    if auth.login(u,p) == "":
        session['user'] = u
        return redirect(url_for("home"))
    else:
        return auth.login(u,p)
    
def reg():
    u = request.form['username']
    p = request.form['password']
    auth.register(u,p)
    return redirect(url_for(login))

@app.route("/home/")
def home():
    return render_template("stories.html", usercontributed = content.get_user_stories(session['user']), usernotcontributed = content.get_no_user_stories(session['user']))
if __name__ == "__main__":
    app.debug = True
    app.run()

@app.route("/logout/")
def logout():
    session.pop('user')
    return redirect(url_for("authenticate"))

@app.route("/new/" methods =["POST", "GET"]):
    if request.method == "GET":
        if 'user' in session:
            return render_template("new.html")
        else:
            return redirect(url_for("authenticate"))
    elif request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        u = session['user']
        content.addstory(u,title,content)
        return redirect(url_for("authenticate"))
    else:
        return error
@app.route("/s/<int:sid>/" methods = "POST")
def story(sid):
    if 'user' not in session:
        return redirect(url_for("authenticate"))
    elif request.method == "POST":
        content.extend_story(session['user'],sid,reqest.form['content'])
        return redirect(url_for("story(" + sid + ")"))
    else:
        if content.user_has_contributed(sid) == True:
            return render_template("story.html", story = content.get_story_full(sid))
        else:
            return render_template("story.html",story = content.get_story_last(sid))



        
