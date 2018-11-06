
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash as hashgen
# CUSTOM MODULES
from extras.greetings import greeting
from utils.validate import validate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'i4d1fr15s8a14'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'aaaaa'
app.config['MYSQL_DATABASE_DB'] = 'querist'

mysql = MySQL()
mysql.init_app(app)
# cursor = mysql.connect().cursor()  # original, obsolete.

conn = mysql.connect()
cursor = conn.cursor()


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
        # MUST add an `if` to abort query execution
        # when non-allowed chars present, thus preventing SQLIA.
        cursor.execute('''
            SELECT id,name FROM usercreds
            WHERE username='{}' AND password='{}';
            '''.format(
                       username,
                       hashgen(hashgen(passwd, method='md5'), method='sha1')))
        match = cursor.fetchone()
        if match is None:
            return render_template('login.html',
                                   title='Log In',
                                   errmsg='''
                                   Username or password not found. Try again
                                   ''',
                                   persist_uname=username)
        else:
            # Using 'else' so that user does NOT login
            # if by any slightest chance `match` != None.
            # On login success:
            session['curr_uid'] = username
            return redirect(url_for('feed'))

    return render_template('login.html', title='Log In')  # show login fields on GET request.


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Signup page is rendered when method == GET;
    # Form data is processed when method == POST;
    # Signup page with flashed message(s) is rendered if input is invalid.
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        passwd = request.form['passwd']
        passwd_conf = request.form['passwd-conf']
        resp, valid_fields, invalid_fields = validate(name,
                                                      username,
                                                      passwd,
                                                      passwd_conf)
        # validate() returns None on success; list of errors and
        # a list of invalid field names on failure.
        if resp is None:
            sql = '''
            INSERT INTO usercreds (username,password,name) VALUES (%s,%s,%s);
            '''
            try:
                cursor.execute(sql, (
                                     username,
                                     hashgen(hashgen(passwd, method='md5'),
                                             method='sha1'),
                                     name))
                # Using two algos reduces success for rainbow tables to work.
                conn.commit()
            except Exception as e:
                return '''
                Something weird happened. We will soon fix it.<br/>
                Click <a href="{{url_for('signup')}}">here</a> to retry.
                <br/>The error was : <br/><span style="color:red;">{}</span>
                '''.format(e)
            session['curr_uid'] = username
            return redirect(url_for('feed'))
        # When resp is not None, i.e. invalid input(s) :-
        return render_template('signup.html',
                               valid_fields=valid_fields,
                               invalid_fields = invalid_fields,
                               title='Sign Up')

    return render_template('signup.html', title='Sign Up')  # Show signup-form on GET request.


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
        return render_template('feed.html',
                               status='Sorry. No posts to show.',
                               title='Quick Feed')
    # If session is not defined, i.e user did not log in,
    # and attmepts to directly view the feed :-
    return render_template('login.html',
                           errmsg='Please log in to continue.')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
