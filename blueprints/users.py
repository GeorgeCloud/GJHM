from flask import Blueprint, render_template, request, url_for, redirect, session
from extensions import find_movie
from datetime import datetime
from db import *
import uuid

users_bp = Blueprint('users_bp', __name__, template_folder='templates')

@users_bp.route('/', methods=['GET'])
def index_users():
    all_users = users.find({})

    return render_template('users.html', users=all_users)

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

@users_bp.route('<username>/playlists', methods=['GET', 'POST'])
def index_playlists(username):
    user = users.find_one({'username': username})

    if request.method == 'GET':
        user_playlists = playlists.find({'user_id': user['_id']})
        return render_template('playlists.html', user=user, playlists=user_playlists)
    else:
        playlist = playlists.find_one({'_id': request.form['playlist_id']})
        media_id = request.form['media_id']

        import pdb;pdb.set_trace()

        playlist.update({'$addToSet': {'media_ids': media_id}})

        return redirect(request.referrer)


@users_bp.route('<username>/playlists/new', methods=['GET'])
def new_playlist(username):
    return render_template('playlists_new.html', username=username)

@users_bp.route('<username>/playlists/create', methods=['POST'])
def create_playlist(username):
    # import pdb;pdb.set_trace()
    if session['current_user']['username'] == username:
        time_created_on = datetime.now()
        playlist = {
            '_id':             uuid.uuid4().hex,
            'title':           request.form['title'],
            'user_id':         session['current_user']['_id'],
            'last_updated':    time_created_on,
            'created_on':      time_created_on,
            'media_ids':       [],
            'views':           0
        }

        playlist_id = playlists.insert_one(playlist).inserted_id

        return redirect(url_for('users_bp.view_playlist', username=username, playlist_id=playlist_id))

@users_bp.route('/<username>/playlists/<playlist_id>', methods=['GET'])
def view_playlist(username, playlist_id):
    user = users.find_one({'username': username})

    if not user:
        return 'User not found'

    playlist = playlists.find_one({'_id': playlist_id})

    playlist_media = [find_movie(m.id) for m in playlist['media_ids']]

    return render_template('playlists_show.html', user=user, playlist=playlist, media=playlist_media)  #, playlists=user_playlists

# @users_bp.route('/<username>/playlists/<playlist_id>', methods=['GET', 'POST'])
# def edit_playlist(username, playlist_id):
#     user = users.find_one({'username': username})
#
#     playlist = playlists.find_one({'_id': playlist_id})
#     import pdb; pdb.set_trace()
#
#     if request.method == 'GET':
#         return render_template('playlists_show.html', user=user, playlist=playlist)  # , playlists=user_playlists
#
#     media_id = request.form['media_id']
#     playlist.update({'$addToSet': { 'media_ids': media_id}})
#
#     return redirect(request.referrer)
