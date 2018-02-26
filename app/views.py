# coding:utf-8


from app import app
from flask import render_template, url_for, request, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
import time


app.secret_key = 'hello world'
app.config['SQLALCHEMY_DATABASE_URI'] = 'root://123:@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "userinfo"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    create_time = db.Column(db.Integer, unique=True)

    def __init__(self, username, password, email, create_time):
        self.username = username
        self.password = password
        self.email = email
        self.create_time = create_time

    def __repr__(self):
        return self.username


@app.route('/', methods=['GET', 'POST'])
def index():
    myname = None
    if 'user_id' in session:
        myname = session['username']
    if request.method == 'GET' and request.args.get('user_id'):
        user_id = request.args.get('user_id')
        sql = ' select * from where user_id = %i' % user_id
        user_list = db.session.execute(sql).fetchall()
    return render_template('index.html', user_list=user_list, myname=myname)


"""
登出
"""


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))


"""
登陆
"""


@app.route('/login', methods=['GET', 'POST'])
def login():
    myname = None
    if request.method == "POST":
        password = request.form['password']
        email = request.form['email']
        if password or email:
            user = User.query.filter_by(email).first()
            if user is not None:
                if user.password != password:
                    flash('Password or email is not ture')
                    return redirect(url_for('login'))
                else:
                    session['user_id'] = user.user_id
                    session['username'] = user.username
                    return redirect(url_for('my_duty'))
            else:
                flash("Password or email is not ture")
                return redirect(url_for('login'))

        else:
            flash('field can not be empty')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', myname=myname)


"""
注册
"""


@app.route('/register', methods=['GET', 'POST'])
def register():
    myname = None
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        repassword = request.form['repassword']
        if username or email or password or repassword:
            if password != repassword:
                flash('Password and Confirm Password not same')
                return redirect(url_for('register'))
            res = User.query.filter_by(email=email).first()
            if res:
                flash('email is be register')
                return redirect(url_for('register'))
            data = User(username, email, password, time.time())
            res = db.session.add(data)
            db.session.commit()
            if data.user_id:
                flash('register successfully! please login')
                return redirect(url_for('login'))
            else:
                flash('register error!')
                return redirect(url_for('register'))
        else:
            flash('field can not be empty')
            return redirect(url_for('register'))
    else:
        return render_template('register.html', myname=myname)


"""
获取
"""


@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        myname = session['username']
        if request.method == 'GET' and request.args.get('user_id'):
            user_id = request.args.get('user_id')
            sql = ' select * from where user_id = %i' % user_id
            user_list = db.session.execute(sql).fetchall()
        return render_template('user.html', user_list=user_list, myname=myname)


"""
修改
"""


@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        myname = session['username']
        if request.method == 'POST':
            name = request.form['name']
            if name:
                res = update_user.query.filter_by(name=name).first()
                if res:
                    return redirect(url_for('update_user'))
                else:
                    data = update_user(name)
                    res = db.session.add(data)
                    db.session.commit()
                    return redirect(url_for('user'))
        return render_template('update_user.html', username=session['username'], myname=myname)


@app.errorhandler(404)
def page_not_found(e):
    myname = None
    if 'user_id' in session:
        myname = session['username']
    return render_template('404.html', myname=myname), 404


@app.errorhandler(500)
def internal_server_error(e):
    myname = None
    if 'user_id' in session:
        myname = session['username']
    return render_template('500.html', myname=myname), 500
