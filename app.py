from flask import Flask, session, render_template, request, redirect
import os, db_manager.py

Story = Flask(__name__)
Story.secret_key = os.urandom(64)

def loggedIn(input_user, input_pass):
        if db_manager.user_exist(input_user):
                if db_manager.user_pass(input_user) == input_pass:
                        session['username'] = input_user
                        return True
        return False

@Story.route('/')
def root():
        if loggedIn():
                return render_template("home.html")
        else:
                return render_template("login.html")


@Story.route('/login')
def login():
	return render_template("login.html")


@Story.route('/edit', methods = ['GET', 'POST'])
def edit():
        return render_template("edit.html")

if __name__ == "__main__":
    Story.debug = True
    Story.run()
