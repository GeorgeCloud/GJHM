from flask import Blueprint, render_template, request, url_for, redirect
from bson.objectid import ObjectId
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

    if not user:
        return 'User not found'

    # user_playlists = playlists.find_many({'creator_username': username})

    return render_template('users_show.html', user=user)  #, playlists=user_playlists

@users_bp.route('<username>/edit', methods=['GET', 'POST'])
def edit_user(username):
    """ Edit and Update Route """
    pass

@users_bp.route('<username>/delete', methods=['POST'])
def delete_user(username):
    users.find_one_and_delete({'username': username})
    return 'user deleted'

@users_bp.route('<username>/playlists', methods=['GET'])
def index_playlists(username):
    user = users.find_one({'username': username})
    user_playlists = playlists.find({'created_by_name': username})

    return render_template('playlists.html', user=user, playlists=user_playlists)

@users_bp.route('<username>/playlists/new', methods=['GET'])
def new_playlist(username):
    return render_template('playlists_new.html', username=username)

@users_bp.route('<username>/playlists/create', methods=['POST'])
def create_playlist(username):
    time_created_on = datetime.now()
    playlist = {
        'title':           request.form['title'],
        'created_by_name': username,
        'last_updated':    time_created_on,
        'created_on':      time_created_on,
        'views':           0
    }

    playlist_id = playlists.insert_one(playlist).inserted_id

    return redirect(url_for('users_bp.view_playlist', username=username, playlist_id=playlist_id))

@users_bp.route('/<username>/playlists/<playlist_id>', methods=['GET'])
def view_playlist(username, playlist_id):
    user = users.find_one({'username': username})

    if not user:
        return 'User not found'

    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})

    return render_template('playlists_show.html', user=user, playlist=playlist)  #, playlists=user_playlists
