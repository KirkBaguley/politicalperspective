import time
from flask import Flask, redirect, url_for, render_template, request, session, flash
from articlesdb import ArticleDB
from usersdb import UserDB
from passlib.hash import bcrypt
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "MambaForever"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/", methods=["POST","GET"])
def home():
    session["button_id"] = 1
    db = ArticleDB()
    likeArticles = db.getAllLikeArticles()
    return render_template("index.html", articles = likeArticles)

@app.route("/index.html")
def index():
    return redirect(url_for("home"))

@app.route("/reading", methods=["POST","GET"])
def reading():
    db = ArticleDB()
    likeArticles = db.getAllLikeArticles()
    i = session["button_id"]
    i = int(i)
    likeArticle = likeArticles[i-1]
    return render_template("reading.html", article = likeArticle )

@app.route("/prereading", methods=["POST","GET"])
def prereading():
    if request.method == "POST":
        ids = request.form.get("article")
        session["button_id"] = ids
        return redirect(url_for("reading"))

@app.route("/prereading2", methods=["POST","GET"])
def prereading2():
    if request.method == "POST":
        if request.form.get("perspectives") == "Liberal":
            return redirect(url_for("liberal"))
        elif request.form.get("perspectives") == "Independent":
            return redirect(url_for("independent"))
        elif request.form.get("perspectives") == "Conservative":
            return redirect(url_for("conservative"))
        else:
            return redirect(url_for("reading"))

@app.route("/liberal", methods=["POST","GET"])
def liberal():
    db = ArticleDB()
    likeArticles = db.getAllLikeArticles()
    i = session["button_id"]
    i = int(i)
    likeArticle = likeArticles[i-1]
    return render_template("liberal.html", article = likeArticle )

@app.route("/independent", methods=["POST","GET"])
def independent():
    db = ArticleDB()
    likeArticles = db.getAllLikeArticles()
    i = session["button_id"]
    i = int(i)
    likeArticle = likeArticles[i-1]
    return render_template("independent.html", article = likeArticle )

@app.route("/conservative", methods=["POST","GET"])
def conservative():
    db = ArticleDB()
    likeArticles = db.getAllLikeArticles()
    i = session["button_id"]
    i = int(i)
    likeArticle = likeArticles[i-1]
    return render_template("conservative.html", article = likeArticle )

@app.route("/login", methods=["POST","GET"])
def login():
    db = UserDB()
    if request.method == "POST":
        email = request.form['lemail']
        password = request.form['lpassword']
        user = db.getOneUser(email)
        if user != None:
            pdict = db.verifyUser(email)
            test = pdict['password']
            if bcrypt.verify(password, test):
                flash('You have successfully logged in!',"info")
                session["user"] = email
                return redirect(url_for("home"))
            else:
                flash('Password Incorrect',"info")
                return render_template("login.html")
        else:
            flash('Username or Password incorrect',"info")
            return render_template("login.html")
    else:
        if "user" in session:
            flash("You're already logged in","info")
            return redirect(url_for("home"))    
        return render_template("login.html")


@app.route("/signup", methods=["POST","GET"]) 
def signup():
    db = UserDB()
    if request.method == "POST":
        fname = request.form["sfname"]
        lname = request.form["slname"]
        age = request.form["sage"]
        email = request.form["semail"]
        password = request.form["cspassword"]
        epassword = bcrypt.hash(password)
        password = None
        user = db.getOneUser(email)
        if user == None:
            db.insertUser(fname,lname,age,email,epassword)
            flash("User created","info")
            return redirect(url_for("login"))
        else:
            flash("User already exists","info")
            return render_template("signup.html")
    else:
        return render_template("signup.html")

@app.route("/logout")
def logout():
    session["user"] = None
    flash("You have been logged out","info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run()