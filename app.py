
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash as hashgen
from werkzeug import check_password_hash as chk
# CUSTOM MODULES
from extras.greetings import greeting
from utils.validate import validate
from db_config import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'i4d1fr15s8a14'
app.config['MYSQL_DATABASE_HOST'] = db['host']
app.config['MYSQL_DATABASE_USER'] = db['user']
app.config['MYSQL_DATABASE_PASSWORD'] = db['password']
app.config['MYSQL_DATABASE_DB'] = db['name']

mysql = MySQL()
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

# custom variables..
logged_in = False  # default, logged out.


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', greeting=greeting, title='Home')


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
        sql = "SELECT username,password FROM usercreds WHERE username='{}';"
        cursor.execute(sql.format(username))
        match = cursor.fetchone()
        if match is not None:
            _passwd = match[1]  # hashed pswd..
            if not chk(_passwd, passwd):
                return render_template('login.html',
                                        title='Log In',
                                        errmsg='Invalid credentials. Please try again.',
                                        persist_uname=username)
            else:
                # using else so that user does NOT login
                # if by any slightest chance `match` != None.
                # On login success:
                session['curr_uid'] = username
                global logged_in; logged_in = True
                return redirect(url_for('feed'))
        elif match is None:
            return render_template('login.html',
                                    title='Log In',
                                    errmsg='Invalid credentials. Please try again.',
                                    persist_uname=username)

    if request.method == 'GET':
        errmsg = request.args.get('errmsg')
        return render_template('login.html',
                                errmsg=errmsg,
                                title='Log In')




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Signup page is rendered when method == GET;
    # Form data is processed when method == POST;
    # Signup page with flashed message(s) is rendered if input is invalid.
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        passwd = request.form['passwd']
        valid = validate(name, username, passwd)
        if valid == 1:
            # checking if username exists or not..
            sql = "SELECT id FROM usercreds WHERE username='{}';"
            cursor.execute(sql.format(username))
            match = cursor.fetchone()
            if match is None:
                sql = "INSERT INTO usercreds (username,password,name) VALUES (%s,%s,%s);"
                try:
                    cursor.execute(sql, (username,
                                         hashgen(passwd, method='sha1'),
                                         name))
                    conn.commit()
                except Exception as e:
                    return '''
                    Something weird happened. We will soon fix it.<br/>
                    Click <a href="{{url_for('signup')">here</a> to retry.
                    '''
                session['curr_uid'] = username
                global logged_in; logged_in = True
                return redirect(url_for('feed'))
            else:
                # when username exists..
                return render_template('signup.html',
                                        title='Sign Up',
                                        errmsg='Username unavailable')
        else:
            return render_template('signup.html',
                                    title='Sign Up',
                                    errmsg='Invalid fields!')
    if request.method == 'GET':
        return render_template('signup.html', title='Sign Up')




@app.route('/feed', methods=['GET', 'POST'])
def feed():
    if logged_in:
        cursor.execute("SELECT author,body FROM posts;")
        posts = cursor.fetchall()
        if posts is not None:
            return render_template('feed.html',
                                    title='Quick Feed',
                                    posts=posts,
                                    me=session['curr_uid'])
        return render_template('feed.html',
                                status='Sorry. No posts to show.',
                                title='Quick Feed')
    # if user not logged in..
    return redirect(url_for('login',
                            errmsg='You must log in to continue.'))



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
