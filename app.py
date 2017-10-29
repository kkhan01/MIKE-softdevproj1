from flask import Flask, session, render_template, request, redirect, flash,  url_for
import os

import sqlite3   #enable control of an sqlite database


f="data/database.db"

db = sqlite3.connect(f, check_same_thread=False) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
#all functions in this file
#$ grep -i 'keyword' db_manager.py
'''
def builder(tablename,args):
def story_exists(storyname):
def make_story(storyname):
def user_exist(username):
def add_user(username, password):
def story_users(storyname,user):
def add_edit(storyname, edit, username):
def get_edit(storyname):
'''

#makes database basics
def builder(tablename,args):
    command = "CREATE TABLE %s (%s);" %(tablename, args)
    c.execute(command)
    return

#checks if a table exists in the database
def story_exists(storyname):
    command = "SELECT name FROM sqlite_master WHERE type='table' AND name='%s';" %(storyname)
    ans = c.execute(command)
    for i in ans:
        return i[0] == storyname
    else:
        return False

#makes the basic structure if nonexistent
if(story_exists("___users") == False):
    builder("___users", "username TEXT UNIQUE, password TEXT")

#makes story with storyname if nonexistent
#should be checked by flask, maybe flash msg
def make_story(storyname):
    if(story_exists(storyname) == True):
        return storyname + ' EXISTS'
    command = "CREATE TABLE %s (edits TEXT, username TEXT UNIQUE);" %(storyname)
    c.execute(command)
    return storyname + " CREATED"

#checks if username is in db
def user_exist(username):
    command = 'SELECT * FROM ___users'
    possibility = c.execute(command)
    for i in possibility:
        if(i[0] == username):
            return True
    return False

#gets a username's pass
def user_pass(username):
    command = 'SELECT * FROM ___users'
    possibility = c.execute(command)
    for i in possibility:
        if(i[0] == username):
            return i[1]
    return False

#adds a username + pass to the ___users db
def add_user(username, password):
    if not user_exist(username):
        command = 'INSERT INTO ___users VALUES("%s", "%s")'%(username, password)
        c.execute(command)
        return True
    else:
        return False

#return if user editted story
def story_users(storyname, user):
    command = 'SELECT username FROM %s'%storyname
    possibility = c.execute(command)
    for i in possibility:
        if(i[0] == username):
            return True
    else:
        return False

#adds edit to story database
#checking of file + user will be in flask app
def add_edit(storyname, edit, username):
    command = 'INSERT INTO %s VALUES("%s", "%s", %d)'%(storyname, edit, username, lastnum(storyname))
    c.execute(command)

#get last edit from story
def get_edit(storyname):
    command = 'SELECT * FROM %s'%storyname
    records = c.execute(command)
    line = ''
    for record in records:
        line = record[0]
    return line

#get last edit's username
def get_user(storyname):
    command = 'SELECT * FROM %s'%storyname
    records = c.execute(command)
    line = ''
    for record in records:
        line = record[1]
    return line

#get all stories a user edited
def user_stories(username):
    stories = {}
    command = "SELECT name FROM sqlite_master WHERE type='table' AND name='%s';" %(storyname)
    ans = c.execute(command)
    for i in ans:
        if(i[0] != '___users' and story_users(i[0], username)):
            stories.append(i[0])
    return stories

#==========================================================

app = Flask(__name__)
app.secret_key = os.urandom(64)

@app.route('/', methods = ['GET','POST'])
def root():
        if 'username' in session:
            return render_template("home.html")
        elif request.method == 'POST':
            #debugging
            print request.form["username"]
            print request.form["password"]
            print user_exist(request.form["username"])
            print user_pass(request.form["username"])
            
            if user_exist(request.form["username"]):
                flash("Invalid username")
                return render_template('login.html')
            elif user_pass(request.form["username"]) != request.form["password"]:
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
    elif user_exist(request.form["username"].strip()):
        flash("username exist")
        return render_template('create.html')
    elif request.form["password"].strip() == "":
        flash("No password - No Spaces Please")
        return render_template('create.html')
    elif request.form["npassword"].strip() == "":
        flash("Re-type password - No Spaces Please")
        return render_template('create.html')
    elif request.form["password"].strip() != request.form["npassword"]:
        flash("Password Don't Match, Try Again")
        return render_template('create.html')
    elif (request.form["password"] == request.form["npassword"]) and request.form["password"].strip() != "":
        new_user = request.form["username"]
        password = request.form["password"]
        add_user(new_user, password)
        return render_template('login.html', msg = "Account Made")
    else:
        flash("Somthing Went Wrong, Try Again")
        return render_template('create.html')


if __name__ == "__main__":
    app.debug = True
    app.run()

#==========================================================
db.commit() #save changes
db.close() #close database
