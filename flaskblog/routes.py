from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(form.username.data, form.email.data, hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('hello'))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('hello'))


@app.route('/account')
@login_required
def account():
    image_file = url_for('static', filename=current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file)
