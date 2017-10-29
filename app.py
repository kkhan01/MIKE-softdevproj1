from flask import Flask, session, render_template, request, redirect, flash,  url_for
import os
from utils import db_manager

app = Flask(__name__)
app.secret_key = os.urandom(64)

@app.route('/', methods = ['GET','POST'])
def root():
        if 'username' in session:
            return render_template("home.html")
        elif request.method == 'POST':

            if request.form["username"] != "username":
                flash("Invalid username")
                return render_template('login.html')
            elif request.form["password"] != "password":
                flash("Invalid password")
                return render_template('login.html')
            else:
                session["username"] = request.form["username"] # Store username
                return render_template('home.html', user = session["username"])
        #elif
        return render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop("username");
    return redirect( url_for('root') )

@app.route('/edit')
def edit():
    if 'username' in session:
        return render_template("edit.html")
    else:
        return redirect( url_for('root') )

@app.route('/magic', methods = ["POST"])
def magic():
    if 'username' in session:
        new_edit = request.form["story_edit"]
        return render_template('home.html', user = session["username"])
    else:
        return redirect( url_for('root') )

@app.route('/create')
def create():
    return render_template("create.html")


@app.route('/creator', methods = ["POST"])
def creator():
    if request.form["username"].strip() == "":
        flash("No username - No Spaces Please")
        return render_template('create.html')
    elif request.form["username"].strip() == "username":
        flash("username exist")
        return render_template('create.html')
    elif request.form["password"].strip() == "":
        flash("No password - No Spaces Please")
        return render_template('create.html')
    elif request.form["npassword"].strip() == "":
        flash("Re-type password - No Spaces Please")
        return render_template('create.html')
    elif request.form["username"].strip() != request.form["npassword"]:
        flash("Password Don't Match, Try Again")
        return render_template('create.html')
    elif (request.form["password"] == request.form["npassword"]) and request.form["password"].strip() != "":
        new_user = request.form["username"]
        password = request.form["password"]
        return render_template('login.html', msg = "Account Made")
    else:
        flash("Somthing Went Wrong, Try Again")
        return render_template('create.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
