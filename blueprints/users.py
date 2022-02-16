from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from extensions import find_movie, is_publisher
from datetime import datetime
from db import *
import uuid

users_bp = Blueprint('users_bp', __name__, template_folder='templates')

@users_bp.route('/', methods=['GET'])
def index_users():
    return render_template('users.html', users=users.find({}))

@users_bp.route('/<username>', methods=['GET'])
def view_user(username):
    user = users.find_one({'username': username})
    if not user:
        return 'User not found'

    user_playlists = playlists.find({'user_id': user['_id']})
    return render_template('users_show.html', user=user, playlists=user_playlists)

@users_bp.route('<username>/edit', methods=['GET', 'POST'])
def edit_user(username):
    """ Edit and Update Route """
    pass

@users_bp.route('<username>/delete', methods=['POST'])
def delete_user(username):
    users.find_one_and_delete({'username': username})
    return 'user deleted'

@users_bp.route('<username>/playlists/new', methods=['GET'])
def new_playlist(username):
    return render_template('playlists_new.html', username=username)

@users_bp.route('<username>/playlists/create', methods=['POST'])
def create_playlist(username):
    if session['current_user']['username'] == username:
        time_created_on = datetime.now()
        playlist = {
            '_id':             uuid.uuid4().hex,
            'title':           request.form['title'],
            'description':     request.form['description'],
            'user_id':         session['current_user']['_id'],
            'last_updated':    time_created_on,
            'created_on':      time_created_on,
            'media_ids':       [],
            'views':           0
        }

        playlist_id = playlists.insert_one(playlist).inserted_id
        return redirect(url_for('users_bp.view_playlist', username=username, playlist_id=playlist_id))

@users_bp.route('<username>/playlists', methods=['GET'])
def view_user_playlists(username):
    user = users.find_one({'username': username})

    user_playlists = playlists.find({'user_id': user['_id']})
    return render_template('playlists.html', user=user, playlists=user_playlists)

@users_bp.route('<username>/playlists', methods=['POST'])
def update_playlist(username):
    if is_publisher(username):
        media_id = request.form['media_id']
        playlist_id = request.form['playlist_id']

        playlists.update_one(
            {'_id': playlist_id},
            {'$addToSet': {'media_ids': media_id}}
        )

        flash('Successfully added to playlist.')
        return redirect(request.referrer)

@users_bp.route('/<username>/playlists/<playlist_id>', methods=['GET'])
def view_playlist(username, playlist_id):
    user = users.find_one({'username': username})
    if not user:
        return 'User not found'

    playlist = playlists.find_one({'_id': playlist_id})
    playlist_media = [find_movie(media_id) for media_id in playlist['media_ids']]

    return render_template('playlists_show.html', user=user, playlist=playlist, media=playlist_media)  #, playlists=user_playlists
