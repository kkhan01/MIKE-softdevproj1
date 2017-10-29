from flask import Flask, session, render_template, request, redirect, flash,  url_for
import os
from utils import db_manager

Story = Flask(__name__)
Story.secret_key = os.urandom(64)

@Story.route('/', methods = ['GET','POST'])
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

@Story.route('/logout')
def logout():
    if 'username' in session:
        session.pop("username");
    return redirect( url_for('root') )

@Story.route('/edit')
def edit():
    if 'username' in session:
        return render_template("edit.html")
    else:
        return redirect( url_for('root') )

@Story.route('/magic', methods = ["POST"])
def magic():
    if 'username' in session:
        new_edit = request.form["story_edit"]
        return render_template('home.html', user = session["username"])
    else:
        return redirect( url_for('root') )

@Story.route('/create')
def create():
    return render_template("create.html")


if __name__ == "__main__":
    Story.debug = True
    Story.run()
