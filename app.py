
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import url_for

# from flask_sqlalchemy import SQLAlchemy

# CUSTOM MODULES
from extras.greetings import greeting
from extras.usercreds import usercreds
from utils import auth
from utils.validate import validate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'i4d1fr15s8a14'
# app.config['curr_uname'] = None


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', greeting=greeting)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Login page is rendered when method == GET;
    # Form data is processed when method == POST;
    # Login page with a flashed msg is rendered in case of an error.

    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['passwd']
        response = auth.authorise(username, passwd, usercreds)
        # Refer docstrings for utils/auth.py to know about `response` values.
        if response == 1:
            # app.config['curr_uname'] = username
            return redirect(url_for('members'), code=302)
        elif response == 0:
            flash('Incorrect password. Try again.', 'Problem')
            return render_template('login.html', prev_username=username)
        flash('No user named {}. Try again.'.format(username), 'Problem')
        return render_template('login.html')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Signup page is rendered when method == GET;
    # Form data is processed when method == POST;
    # Signup page with flashed message(s) is rendered if input is invalid.
    if request.method == 'GET':
        return render_template('signup.html')
    name = request.form['name']
    username = request.form['username']
    passwd = request.form['passwd']
    response = validate(name, username, passwd)
    if response == 1:
        return redirect(url_for('members'), code=302)
    flash('Some fields too short!')
    return render_template('signup.html')


# ending function
@app.route('/members')
def members():
    # `uid` has to be a session variable.
    return '<h1>Hello, user! You are logged in.</h1>'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
