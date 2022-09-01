from . import api
from .auth import basic_auth
from flask import jsonify, request
from app.models import Post
from app.models import User


@api.route('/token')
@basic_auth.login_required
def get_token():
    return 'Token'


@api.route('/posts', methods=["GET"])
def get_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])


@api.route('/posts/<post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


@api.route('/posts', methods=["POST"])
def create_post():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    # Get the data from the request body
    data = request.json
    print(data, type(data))
    # Validate the data
    for field in ['title', 'body', 'user_id']:
        if field not in data:
            # if field not in request body, respond with a 400 error
            return jsonify({'error': f"'{field}' must be in request body"}), 400
    
    # Get fields from data dict
    title = data.get('title')
    body = data.get('body')
    user_id = data.get('user_id')
    # Create new instance of post with data
    new_post = Post(title=title, body=body, user_id=user_id)
    return jsonify(new_post.to_dict()), 201

    # update to have a create user route and get user route
    # - [POST] api/users/ - Create a New User
    # [GET] /api/users/<id> - Get an Exsitsing User


# get a user by id
@api.route('users/<user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

# create a new user:
@api.route('/users', methods=["POST"])
def create_user(user_id):
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    # Get the data from the request body
    data = request.json
    # Validate the data
    for field in ['email', 'username', 'password']:
        if field not in data:
            # if field not in request body, respond with a 400 error
            return jsonify({'error': f"'{field}' must be in request body"}), 400
    
    # Get method refers to the primary key. That is what you will want to put into the params
    # Get fields from data dict
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
     # Before we add the user to the database, check to see if there is already a user with username or email
    existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
    if existing_user:
        return jsonify({"error": "User with username and/or email already exists"}), 
        400
     # Create new instance of user with request data    
    new_user = User(email=email, username=username, password=password)
    return jsonify(new_user.to_dict()), 201