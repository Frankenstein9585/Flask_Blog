from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f657b43d1ee366f7cdc9912fd484f8d0'
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
