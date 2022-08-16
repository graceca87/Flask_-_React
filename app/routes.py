from app import app
from flask import render_template
from app.forms import SignUpForm


@app.route('/')
def index():
    user_info = {
        'username': 'brians',
        'email': 'brians@codingtemple.com'
    }
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    return render_template('index.html',user=user_info, colors=colors)


@app.route('/signup')
def signup():
    form = SignUpForm()
    return render_template('signup.html', form=form)
