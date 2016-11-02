import flask
import auth
import content
app = Flask(__name__)


@app.route("/")
def authenticate():
    if user in session:
        return redirect(url_for("home"))
    else:
        
return redirect(url_for("login"))
app.route("/login", methods = ["POST"])
def auth():
    if 'login' in request.form:
        return login()
    else:
        return reg()

def login():
    u = request.form['username']
    p = request.form['password']
    if 
