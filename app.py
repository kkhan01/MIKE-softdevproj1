from flask import Flask, session, render_template, request, redirect
import os

Story = Flask(__name__)
#login.secret_key = os.urandom(64)

@Story.route('/', methods = ['GET', 'POST'])
def root():
	return render_template("login.html")


@Story.route('/edit', methods = ['GET', 'POST'])
def edit():
        return render_template("edit.html")






if __name__ == "__main__":
    Story.debug = True
    Story.run()
