from flask import Blueprint, render_template, request, url_for, redirect
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
        'email':      request.form['email'],
        'first_name': request.form['first_name'],
        'last_name':  request.form['last_name'],
        'password':   request.form['password'],
        'avatar_url': '',
        'created_on': datetime.now(),
    }

    user_id = users.insert_one(user).inserted_id

    return redirect(url_for('users_bp.view_user', user_id=user_id))

@users_bp.route('<user_id>/edit', methods=['GET'])
def edit_user(user_id):
    return 'edit page'

@users_bp.route('<user_id>/update', methods=['POST'])
def update_user():
    return 'update page'

@users_bp.route('/<user_id>', methods=['GET'])
def view_user(user_id):
    user = users.find_one({'_id': user_id})

    return render_template('users_show.html', user=user)
