import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O


f="../data/database.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
#makes database basics
def builder(tablename,args):
    command = "CREATE TABLE %s (%s);" %(tablename, args)
    #print command
    c.execute(command)
    #debugging
    cursor = db.execute('select * from ___users')
    colnames = cursor.description
    fields = ''
    print '___users fields:'
    for row in colnames:
        fields+= row[0] + '\t'
    print fields
    return

#checks if a table exists in the database
def story_exists(storyname):
    command = "SELECT name FROM sqlite_master WHERE type='table' AND name='%s';" %(storyname)
    ans = c.execute(command)
    for i in ans:
        return i[0] == storyname
    else: return False

#makes the basic structure if nonexistent
if(story_exists("___users") == False):
    builder("___users", "username TEXT UNIQUE, password TEXT")
#testing
'''
print story_exists("haha")
print story_exists("users")
'''

def make_story(storyname):
    if(story_exists(storyname) == True):
        return storyname + ' EXISTS'
    command = "CREATE TABLE %s (edits TEXT, username TEXT UNIQUE);" %(storyname)
    c.execute(command)
    #debugging
    '''
    cursor = db.execute('select * from %s'%storyname)
    colnames = cursor.description
    fields = ''
    print storyname + ' fields:'
    for row in colnames:
        fields+= row[0] + '\t'
    print fields
    '''
    return storyname + " CREATED"

#more testing
'''
for i in range (1,11):
    make_story('abc'+str(i))
'''


#==========================================================
db.commit() #save changes
db.close() #close database
