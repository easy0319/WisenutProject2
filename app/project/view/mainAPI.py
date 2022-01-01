from flask import Blueprint, Flask, render_template

mainAPI = Blueprint('mainAPI', __name__, template_folder='templates')

@mainAPI.route('/')
def base():
    return render_template('base.html')

@mainAPI.route('/signin')
def signin():
    return render_template('signin.html')

@mainAPI.route('/signup')
def signup():
    return render_template('signup.html')