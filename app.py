
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
from utils.validate import validate
# from utils.db_ops import query

app = Flask(__name__)
app.config['SECRET_KEY'] = 'i4d1fr15s8a14'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'aaaaa'
app.config['MYSQL_DATABASE_DB'] = 'enleren'

mysql = MySQL()
mysql.init_app(app)
cursor = mysql.connect().cursor()

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
        cursor.execute("SELECT id,name FROM usercreds WHERE username='{}' AND password='{}';"
                       .format(username, passwd))
        match = cursor.fetchone()
        if match is None:
            flash('Invalid Credentials.', 'Error')
            return render_template('login.html', title='Log In', prev_uname=username)
        else:
            # using else so that user does NOT login
            # if by any chance `match` != None;
            session['curr_uid'] = username
            return redirect(url_for('feed'))

    return render_template('login.html')  # show login fields on GET..


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
            session['curr_uid'] = username
            return redirect(url_for('feed'), code=302)
        flash('Some fields too short!', 'Invalid')
        return render_template('signup.html', title='Sign Up')

    if request.method == 'GET':
        return render_template('signup.html')


@app.route('/feed', methods=['GET', 'POST'])
def feed():
    if session['curr_uid']:
        cursor.execute("SELECT author,body FROM posts;")
        posts = cursor.fetchall()
        if posts is not None:
            return render_template('feed.html',
                                    title='Quick Feed',
                                    posts=posts,
                                    me=session['curr_uid'])
        return render_template('feed.html', status='Sorry. No posts to show :(')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
