import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O


f="../data/database.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
#INSERT YOUR POPULATE CODE IN THIS ZONE
def builder(tablename,args):
    command = "CREATE TABLE %s (%s);" %(tablename, args)
    #print command
    c.execute(command)
    #debugging
    '''
    cursor = db.execute('select * from users')
    colnames = cursor.description
    for row in colnames:
        print row[0]
    '''
    return

builder("users", "username TEXT UNIQUE, password TEXT")

#==========================================================
db.commit() #save changes
db.close() #close database
