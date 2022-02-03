from flask import Blueprint, render_template
from datetime import datetime
from db import *

users_bp = Blueprint('users_bp', __name__, template_folder='templates')

@users_bp.route('/', methods=['GET'])
def index_users():
    return render_template('users.html')

@users_bp.route('/new', methods=['GET'])
def new_user():
    return render_template('users_new.html')

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

    user_id = db.users.insert_one(user).inserted_id

    return render_template('users_show.html', user_id=user_id)

@users_bp.route('/edit', methods=['GET'])
def edit_user():
    return 'edit page'

@users_bp.route('/update', methods=['POST'])
def update_user():
    return 'update page'

@users_bp.route('/<user_id>', methods=['GET'])
def view_user(user_id):
    return f'user_id: {user_id}'
