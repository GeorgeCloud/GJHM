from flask import Blueprint, render_template, request, url_for, redirect, session, flash
import flask
from extensions import find_movie, current_user_is, login_required, find_user, user_playlists, current_user
from datetime import datetime
from db import *
import uuid

users_bp = Blueprint('users_bp', __name__, template_folder='templates')

@users_bp.route('/', methods=['GET'])
def index_users():
    return render_template('users.html', users=users.find({}))


@users_bp.route('/<username>', methods=['GET'])
def view_user(username):
    user = find_user(username)
    user_current = current_user()
    requested = False
    if not user:
        return 'User not found'

    u_playlists = user_playlists(user['_id'])
    u_reviews = reviews.find({'user_id': user['_id']})

    friends = user['friends']

    if user_current:
        for invite in friend_requests.find():
            if invite['sender_id'] == user_current['_id'] and invite['reciever_id'] == user['_id']:
                requested = True

    return render_template('users_show.html', user=user,
                                              user_current=user_current,
                                              playlists=u_playlists,
                                              requested=requested,
                                              friends=friends,
                                              reviews=u_reviews
                                              )

@users_bp.route('<username>/edit', methods=['GET', 'POST'])
def edit_user(username):
    """ Edit and Update Route """
    pass

@users_bp.route('<username>/delete', methods=['POST'])
@login_required
def delete_user(username):
    if current_user_is(username):
        session.clear()
        users.find_one_and_delete({'username': username})
        flash('Successfully Deleted Account.')
    else:
        flash('You are not the owner of this account')

    return redirect(url_for('homepage'))


@users_bp.route('<username>/playlists/new', methods=['GET'])
@login_required
def new_playlist(username):
    return render_template('playlists_new.html', username=username)

@users_bp.route('<username>/playlists/create', methods=['POST'])
@login_required
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
        return redirect(url_for('users_bp.view_single_playlist', username=username, playlist_id=playlist_id))

@users_bp.route('<username>/playlists', methods=['GET'])
def view_user_playlists(username):
    user = find_user(username)
    users_plist = user_playlists(user['_id'])

    return render_template('playlists.html', user=user, playlists=users_plist)

@app.route('/playlists/<playlist_id>', methods=['GET'])
@users_bp.route('/<username>/playlists/<playlist_id>', methods=['GET'])
def view_single_playlist(playlist_id, username=None):
    playlist = playlists.find_one({'_id': playlist_id})
    user = find_user(username, user_id=playlist['user_id'])

    plist_media = [find_movie(media_id) for media_id in playlist['media_ids']]  # return list of movie/tvshows from user's playlist

    return render_template('playlists_show.html', user=user, playlist=playlist, media_result=plist_media)

@users_bp.route('<username>/playlists', methods=['POST'])
@login_required
def update_playlist(username):
    if current_user_is(username):
        media_id = request.form['media_id']
        playlist_id = request.form['playlist_id']

        playlists.update_one(
            {'_id': playlist_id},
            {'$addToSet': {'media_ids': media_id}}
        )

        flash('Successfully added to playlist.')
    return redirect(request.referrer)


@users_bp.route('/<username>/playlists/<playlist_id>', methods=['POST'])
@login_required
def delete_playlist(username, playlist_id):
    if current_user_is(username):
        playlists.find_one_and_delete({'_id': playlist_id})
        flash('Successfully Deleted Playlist.')
    else:
        flash('You are not the owner of this playlist')

    return redirect(url_for('homepage'))




@users_bp.route('<friend_username>/request-friend/<username>', methods=['POST', 'GET'])
def new_invitation(friend_username, username):
    """Request another user as a friend"""
    user_current = users.find_one({'username': username})
    user_requested = users.find_one({'username': friend_username})
    invitation = {
        '_id': uuid.uuid4().hex,
        'sender_id': user_current['_id'],
        'reciever_id': user_requested['_id'],
        'date': datetime.now()
    }
    friend_requests.insert_one(invitation)
    return redirect(url_for('users_bp.view_user', username=friend_username))

@users_bp.route('/<username>/friend-requests', methods=['GET', 'POST'])
def view_invitations(username):
    """able to accept or deny here"""
    """TODO: If accepted, add to user's friends dictionary"""
    requests = []
    user = users.find_one({'username': username})
    user_invitations = friend_requests.find({'reciever_id': user['_id']})
    # iterating over each invite and finding user info then adding to requests list
    for invite in user_invitations:
        sender = users.find_one({'_id': invite['sender_id']})
        requests.append(sender)
    return render_template('users_friend_requests.html', user=user, requests=requests)

@users_bp.route('/<username>/friend-requests/delete', methods=['GET', 'POST'])
def delete_invitation(username):
    user = users.find_one({'username': username})
    if flask.request.method == 'POST':
        friend_requests.find_one_and_delete({'sender_id': request.form.get('invitation_id')})
    return redirect(url_for('users_bp.view_invitations', username=user['username']))

@users_bp.route('/<username>/friend-requests/accept', methods=['GET', 'POST'])
def accept_invitation(username):
    user = users.find_one({'username': username})
    friend = users.find_one({'username': request.form.get('friend_username')})
    if flask.request.method == 'POST':
        # delete friend request and append friend object to current user's
        friend_requests.find_one_and_delete({'sender_id': request.form.get('invitation_id')})
        users.update_one(
            {'username': friend['username']},
            {'$push': {'friends': user['_id']}}
        )
        users.update_one(
            {'username': username},
            {'$push': {'friends':friend['_id']}}
        )
    return redirect(url_for('users_bp.view_invitations', username=user['username']))

@users_bp.route('/<username>/friends', methods=['GET'])
def view_friends(username):
    user=users.find_one({'username':username})
    friends=user['friends']
    friends_list = []
    for id in friends:
        friends_list.append(users.find_one({'_id':id}))
    return(render_template('users_friends_index.html', user=user, friends=friends_list))

@users_bp.route('/<username>/reviews', methods=['GET'])
def user_reviews():
    reviews.find({''})
    return(render_template('users_friends_index.html', user=user, friends=friends_list))

@users_bp.route('/<username>/friends/delete', methods=['POST'])
def delete_friend(username):
    """Remove logged in user's friend"""
    """Can only be done by matching user/if logged in"""
    """Removed friend from user's friend dict"""
    user = users.find_one({'username': username})
    friend = users.find_one({'username': request.form.get('friend_username')})
    print(friend)
    print(user)
    users.update_one(
        {'username': friend['username']},
        {'$pull': {'friends': user['_id']}}
    )
    users.update_one(
        {'username': username},
        {'$pull': {'friends': friend['_id']}}
    )
    return redirect(url_for('users_bp.view_friends', username=user['username']))
