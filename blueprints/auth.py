from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import is_authenticated, login_required, logged_out_required, find_user
from datetime import datetime
from db import users, bcrypt
import uuid

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')

@auth_bp.route('/signup', methods=['GET', 'POST'])
@logged_out_required
def signup():
    if request.method == 'POST':
        password = request.form['password']
        user = {
            '_id':        uuid.uuid4().hex,
            'email':      request.form['email'],
            'username':   request.form['username'],
            'full_name':  request.form['full_name'],
            'bio':        request.form['bio'],
            'password':   bcrypt.generate_password_hash(password).decode('utf-8'),
            'avatar_url': '',
            'created_on': datetime.now(),
            'friends': []
        }
        if users.insert_one(user):
            del user['password']
            session['current_user'] = user
            flash('Successfully Signed Up.')
            return redirect(url_for('auth_bp.login'))
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
@logged_out_required
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = find_user(username)

        # Create form validator
        if user and bcrypt.check_password_hash(user['password'], password):
            del user['password']
            session['current_user'] = user
            flash('Logged In')
            return redirect(url_for('homepage'))
    return render_template('login.html')

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    return redirect(url_for('homepage'))
