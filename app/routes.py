from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.forms import SignUpForm, PostForm, LoginForm
from app.models import User, Post


@app.route('/')
def index():
    user_info = {
        'username': 'brians',
        'email': 'brians@codingtemple.com'
    }
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    return render_template('index.html',user=user_info, colors=colors)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    # if the form is submitted and all the data is valid
    if form.validate_on_submit():
        print('Form has been validated! Hooray!!!!')
        email = form.email.data
        username = form.username.data
        password = form.password.data
        # Before we add the user to the database, check to see if there is already a user with username or email
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash('A user with that username or email already exists.', 'danger')
            return redirect(url_for('signup'))
            
        new_user = User(email=email, username=username, password=password)
        flash(f"{new_user.username} has been created.", "success")
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/create', methods=["GET", "POST"])
def create():
    form = PostForm()
    if form.validate_on_submit():
        # Get the data from the form
        title = form.title.data
        body = form.body.data
        # Create a new instance of Post with the form data
        new_post = Post(title=title, body=body, user_id=1)
        # flash a message saying the post was created
        flash(f'{new_post.title} has been created.', 'secondary')
        # Redirect back to home page
        return redirect(url_for('index'))

    return render_template('createpost.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Get username and password from form
        username = form.username.data
        password = form.password.data
        # Query the user table for a user with the same username as the form 
        user = User.query.filter_by(username=username).first()
        # If the user exists and the password is correct for that user
        if user is not None and user.check_password(password):
            # Log the user in with the login_user function from flask_login
            login_user(user)
            # Flash a success message
            flash(f"Welcome back {user.username}!", "success")
            # Redirect back to the home page
            return redirect(url_for('index'))
        # If no user with username or password incorrect
        else:
            # flash a danger message
            flash('Incorrect username and/or password. Please try again.', 'danger')
            # Redirect back to login page
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out.', 'primary')
    return redirect(url_for('index'))
