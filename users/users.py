from flask import Blueprint, render_template
from datetime import datetime
from app import users

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/', methods=['GET'])
def index_users():
    return render_template('index.html')

@users_bp.route('/new', methods=['GET'])
def new_user():
    return 'new user\'s page'

@users_bp.route('/create', methods=['POST'])
def create_user():
    user = {
        'email':      'email@gmail.com',
        'first_name': 'John',
        'last_name':  'Doe',
        'password':   'password',
        'avatar_url': '',
        'created_on': datetime.now(),
    }

    user_id = users.insert_one(user).inserted_id

    return render_template('show_user.html', user_id=user_id)

@users_bp.route('/edit', methods=['GET'])
def edit_user():
    pass

@users_bp.route('/update', methods=['POST'])
def update_user():
    pass
