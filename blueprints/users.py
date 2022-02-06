from flask import Blueprint, render_template, request, url_for, redirect
from datetime import datetime
from db import *

users_bp = Blueprint('users_bp', __name__, template_folder='templates')

@users_bp.route('/', methods=['GET'])
def index_users():
    all_users = users.find({})

    return render_template('users.html', users=all_users)

@users_bp.route('/new', methods=['GET'])
def new_user():
    return render_template('users_new.html')

@users_bp.route('/create', methods=['POST'])
def create_user():
    user = {
        'email':      request.form['email'],
        'username':   request.form['username'],
        'full_name': request.form['full_name'],
        'password':   request.form['password'],
        'avatar_url': '',
        'created_on': datetime.now(),
    }

    users.insert_one(user)

    return redirect(url_for('users_bp.view_user', username=user['username']))

@users_bp.route('/<username>', methods=['GET'])
def view_user(username):
    user = users.find_one({'username': username})
    if user:
        return render_template('users_show.html', user=user)

    return 'User not found'

@users_bp.route('<username>/edit', methods=['GET', 'POST'])
def edit_user(username):
    """ Edit and Update Route """
    pass

@users_bp.route('<username>/delete', methods=['POST'])
def delete_user(username):
    users.find_one_and_delete({'username': username})

    return 'user deleted'
