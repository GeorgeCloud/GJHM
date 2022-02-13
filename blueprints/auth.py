import uuid

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from bson.objectid import ObjectId
from datetime import datetime
from db import users

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    # import pdb;pdb.set_trace()
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        user = {
            '_id':        uuid.uuid4().hex,
            'email':      request.form['email'],
            'username':   request.form['username'],
            'full_name':  request.form['full_name'],
            'password':   request.form['password'],
            'avatar_url': '',
            'created_on': datetime.now(),
        }
        if users.insert_one(user):
            del user['password']
            session['current_user'] = user
            flash('Successfully Signed Up.')

    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        pass
    else:
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({'username': username})

        # Create form validator
        if user and user['password'] == password:
            del user['password']
            session['current_user'] = user
            flash('Logged In')
            return redirect(url_for('homepage'))

    return render_template('login.html')


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('homepage'))
