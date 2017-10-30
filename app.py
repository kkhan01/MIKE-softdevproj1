from __future__ import print_function
from flask import Flask, session, render_template, request, redirect, flash,  url_for
import os
import random
import sqlite3   #enable control of an sqlite database
import threading
import sys

lock = threading.RLock()


f="data/database.db"

db = sqlite3.connect(f, check_same_thread=False) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
#sql code

#all functions in this file
#$ grep -i 'keyword' app.py
'''

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
    command = "CREATE TABLE %s (edits TEXT, username TEXT UNIQUE)" %storyname
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
    command = 'INSERT INTO ___users VALUES("%s", "%s")'%(username, password)
    c.execute(command)
    return True

#admin user
if (user_exist("shanny_boy") == False):
    add_user("shanny_boy", "adminperks")

#return if user editted story
def story_users(storyname, user):
    command = 'SELECT username FROM %s'%storyname
    possibility = c.execute(command)
    for i in possibility:
        if(i[0] == user):
            return True
    else:
        return False
    

#adds edit to story database
#checking of file + user will be in flask app
def add_edit(storyname, edit, username):
    command = 'INSERT INTO %s VALUES("%s", "%s")'%(storyname, edit, username)
    c.execute(command)
    db.commit() #save changes
    return True
    

#get last edit from story
def get_edit(storyname):
    command = 'SELECT * FROM %s'%storyname
    records = c.execute(command)
    line = ''
    for record in records:
        line = record[0]
    return line

#so there's always at least 1 story
if(story_exists("LifeStory") == False):
    make_story("LifeStory")
    add_edit("LifeStory", "Heya! I like to", "shanny_boy")
    db.commit() #save changes

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
    d = db.cursor()    #facilitate db ops
    stories = []
    command = "SELECT name FROM sqlite_master WHERE type='table';"
    ans = d.execute(command)
    for i in ans:
        if(i[0] != '___users' and story_users(i[0], username)):
            stories.append(i[0])
    return stories

#get all stories a user didnt edited
def not_user_stories(username):
    d = db.cursor()    #facilitate db ops
    stories = []
    command = "SELECT name FROM sqlite_master WHERE type='table';"
    ans = d.execute(command)
    for i in ans:
        if(i[0] != '___users' and not story_users(i[0], username)):
            stories.append(i[0])
    return stories

#get all edits to a story
def get_story(storyname):
    story = ''
    command = "SELECT * FROM %s;"%storyname
    ans = c.execute(command)
    for i in ans:
        story += i[0]+'\t--- '+i[1]+';'+' \n'
    return story
#==========================================================
#PRINTS STUFF!!!!
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    return

app = Flask(__name__)
app.secret_key = os.urandom(64)

@app.route('/', methods = ['GET','POST'])
def root():
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if(user_exist(username)):              
            if password == user_pass(username):
                session['username'] = username
                return redirect(url_for ('home'))
            else:
                flash("incorrect Password")
        else:
            flash("incorrect Username/Password")
    return render_template('login.html')
                                         
@app.route('/home')
def home():
    if 'username' in session:
        story = random.choice(not_user_stories(session['username']))
        eprint("CHOSEN STORY: "+ story)
        cuser = session['username']
        allstories = user_stories(cuser)
        return render_template('home.html', user = cuser, stories = allstories, randomstory = story)
    else:
        return redirect(url_for('root'))
        
    

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username');
    return redirect( url_for('root'))

@app.route('/edit', methods = ["GET","POST"])
def edit():
    if 'username' in session and not_user_stories(session['username']):
        story = request.args.get("story")
        eprint(story)
        mostrecent = get_edit(story)
        eprint(mostrecent)
        if request.method == "POST":
            edit = request.form["story_edit"]
            eprint(story)
            add_edit(story,edit, session['username'])
            return redirect(url_for('home'))
        return render_template('edit.html', storyname = story, mostrecentedit = mostrecent )
    else:
        return redirect(url_for('root'))
   

@app.route('/new', methods = ["GET", "POST"])
def new():
    if 'username' in session:
        if request.method == "POST":
            storytitle = request.form["title"]
            firstedit = request.form["story_edit"]
            make_story(storytitle)
            add_edit(storytitle, firstedit, session['username'])
            return redirect( url_for ("home"))
        return render_template("new.html")
    else:
         return redirect(url_for ("root"))

@app.route('/view', methods = ["GET"])
def view():
    if 'username' in session:
        storyn = request.args.get('story')
        storystuff = get_story(storyn)
        return render_template('view.html',story = storystuff, storyname = storyn)
    else:
        return redirect(url_for('root'))
    

'''@app.route('/magic', methods = ["POST"])
def magic():
    if 'username' in session:
        new_edit = request.form["story_edit"]
        eprint(sss, new_edit, session['username'], sep="---")
        add_edit(sss, new_edit, session['username'])
        return render_template('home.html', user = session['username'])
    else:
        return redirect( url_for('root') )'''

@app.route('/create')
def create():
    return render_template("create.html")


@app.route('/creator', methods = ["POST"])
def creator():
    if request.form['username'].strip() == "":
        flash("No username - No Spaces Please")
        return render_template('create.html')
    elif user_exist(request.form["username"].strip()):
        flash("username exist")
        return render_template('create.html')
    elif request.form['password'].strip() == "":
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
        db.commit() #save changes
        return redirect(url_for ('root') )
    else:
        flash("Somthing Went Wrong, Try Again")
        return render_template('create.html')

if __name__ == "__main__":
    app.debug = True
    app.run()

#==========================================================
db.commit() #save changes
db.close() #close database
