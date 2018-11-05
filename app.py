
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import url_for
from flask import session
from flaskext.mysql import MySQL

# CUSTOM MODULES
from extras.greetings import greeting
from extras.usercreds import usercreds
from utils import auth
from utils.validate import validate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'i4d1fr15s8a14'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'aaaaa'
app.config['MYSQL_DATABASE_DB'] = 'enleren'

mysql = MySQL()
mysql.init_app(app)

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
        # add an `if` to abort query execution if non-allowed chars present,
        # thus preventing SQLIA.
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT id FROM usercreds WHERE username='{}' AND password='{}'".format(
                                                                         username, passwd))
        data = cursor.fetchone()
        if data is None:
            return 'Incorrect pair!'
        return 'Logged in successfully!'

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Signup page is rendered when method == GET;
    # Form data is processed when method == POST;
    # Signup page with flashed message(s) is rendered if input is invalid.
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        passwd = request.form['passwd']
        response = validate(name, username, passwd)
        if response == 1:
            return redirect(url_for('members'), code=302)
        flash('Some fields too short!')
        return render_template('signup.html')

    if request.method == 'GET':
        return render_template('signup.html')


# ending function
@app.route('/members')
def members():
    # `uid` has to be a session variable.
    return '<h1>Hello, user! You are logged in.</h1>'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
