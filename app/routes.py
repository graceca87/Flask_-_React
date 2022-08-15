from app import app
from flask import render_template


@app.route('/')
def index():
    user_info = {
        'username': 'brians',
        'email': 'brians@codingtemple.com'
    }
    return render_template('index.html',user=user_info)


@app.route('/test')
def test():
    return 'This is a test'
