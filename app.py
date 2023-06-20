from os import getenv
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'f657b43d1ee366f7cdc9912fd484f8d0'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqldb://{}:{}@localhost:3306/{}'.format(HBNB_MYSQL_USER,
                                                                                         HBNB_MYSQL_PWD,
                                                                                         HBNB_MYSQL_DB)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return 'User({} {} {})'.format(self.username, self.email, self.password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return 'Post({} {})'.format(self.title, self.date_posted)


posts = [
    {
        'author': 'Donald Peters',
        'title': 'Post1',
        'content': 'Some random content',
        'date_posted': 'June 19, 2023'
    },

    {
        'author': 'Frankenstein',
        'title': 'Post2',
        'content': 'Some more random content',
        'date_posted': 'June 19, 2023'
    }
]


@app.route('/')
def hello():
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {}!'.format(form.username.data), 'success')
        return redirect(url_for('hello'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'xFrankenstein' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('hello'))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
