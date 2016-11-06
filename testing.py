from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

@app.route("/")
def root():
    #if not logged in:
    return render_template("home.html")
    #if logged in:
    
    ###there should be two options:contributed to and not contributed to
    ###pass two data struct w/ contrib, and non-contrib stories
    ###contrib should have full text,
    ###non-contrib should have latest addition
    #return render_template("stories.html")

    
#fort testing purposes
@app.route("/stories/")
def stories():
    return render_template("stories.html")
    
@app.route("/login/")
def login():
    #if logged in:
    #return redirect("url_for("root"))
    #if not logged in
    return render_template("login.html")


@app.route("/logout/")
def logout():
    # buncha stuff
    return redirect(url_for("root"))

@app.route("/new/")
def new():
    #if not logged in:
    #return redirect(url_for("login"))
    #if logged in:
    return render_template("new.html")

@app.route("/s/<int:sid>")
def story(sid):
    #if not logged in:
    #return redirect(url_for("login"))
    #if logged in:
    ###if it has been contributed to:
    ###pass a data struct w/ title & whole story
    ###if not:
    ###pass a data struct w/ title & latest addition
    ###or some other way idk
    return render_template("story.html")

if __name__ == '__main__':
    app.run(debug = True)
