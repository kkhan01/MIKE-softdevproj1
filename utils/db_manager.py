import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O


f="../data/database.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
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
def story_users(storyname):
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

#adds a username + pass to the ___users db
def add_user(username, password):
    if not user_exist(username):
        command = 'INSERT INTO ___users VALUES("%s", "%s")'%(username, password)
        c.execute(command)
        return True
    else:
        return False

#return list of users who edited a story
def story_users(storyname):
    command = 'SELECT username FROM %s'%storyname
    ret = c.execute(command)
    return ret

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

#==========================================================
db.commit() #save changes
db.close() #close database
