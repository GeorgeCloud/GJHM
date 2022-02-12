from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from bson.objectid import ObjectId
# from db import users

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        pass
    else:
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
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET'])
def login():
    return render_template('signup.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    return render_template('users_new.html')